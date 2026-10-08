<?php
/**
 * Plugin Name: NPCWoods Cache Warm
 * Description: GoDaddy WPaaS bans the whole page cache (gateway + CDN) on every
 *              publish/update. Until pages are re-cached, every crawler request
 *              goes through the GoDaddy gateway rate limiter
 *              (x-gateway-rate-limit-delayed), which queues bursts ~20s and then
 *              answers 503. This re-warms the CDN copy of every sitemap URL in
 *              WP-cron batches a few minutes after each ban, so Googlebot gets
 *              cached 200s instead of 503s. Read-only GETs only.
 * Version: 1.1.0
 * Author: NPCWoods
 *
 * Kitchen source: php/npcwoods-cache-warm.php.
 * 1.0.0 (2026-10-08 crawl fixes): 40-URL batches, 120s cap, 3 timeouts in a row
 *       aborted the batch.
 * 1.1.0 (2026-10-08 tune): MWP cron only ticks every few minutes, so each tick
 *       now does up to 110 URLs inside a 150s wall-clock cap (MWP kills cron at
 *       ~255s). Timeouts/5xx back off (sleep) and keep going instead of
 *       aborting; failed URLs are re-queued once at the end of the walk; the
 *       remainder is rescheduled. A short lock stops two batches overlapping.
 * Kill switch: delete this file. All functions are prefixed npcwoods_cw_.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Seconds to wait after a ban before warming (lets the CDN purge finish). */
function npcwoods_cw_delay() {
	return 240;
}

/** Max URLs per cron run. */
function npcwoods_cw_batch_size() {
	return 110;
}

/** Wall-clock cap per cron run, seconds. Checked before every GET. */
function npcwoods_cw_time_cap() {
	return 150;
}

/** Per-GET timeout, seconds. cap + timeout + max backoff stays well under ~255s. */
function npcwoods_cw_timeout() {
	return 15;
}

/** Pause between good GETs (microseconds). */
function npcwoods_cw_pause_us() {
	return 400000;
}

/** Gap before the next batch when this one ran out of URLs/time normally. */
function npcwoods_cw_batch_gap() {
	return 20;
}

/** Consecutive failures that end a run early (gateway is clearly saturated). */
function npcwoods_cw_max_strikes() {
	return 8;
}

/** Backoff sleep (seconds) after the Nth consecutive failure: 2, 4, 8, 10, 10... */
function npcwoods_cw_backoff( $strikes ) {
	return (int) min( 10, pow( 2, max( 1, (int) $strikes ) ) );
}

function npcwoods_cw_log( $line ) {
	$dir = WP_CONTENT_DIR . '/cache';
	if ( ! is_dir( $dir ) ) {
		return;
	}
	$file = $dir . '/npcwoods-cache-warm.log';
	if ( is_file( $file ) && filesize( $file ) > 262144 ) {
		@rename( $file, $file . '.1' );
	}
	@file_put_contents( $file, gmdate( 'c' ) . ' ' . $line . "\n", FILE_APPEND | LOCK_EX );
}

/** Start (or restart) the warm walk a few minutes from now. */
function npcwoods_cw_schedule( $why ) {
	if ( ! function_exists( 'wp_schedule_single_event' ) ) {
		return;
	}
	// A newer ban makes any in-flight walk stale: restart from the top.
	if ( function_exists( 'wp_unschedule_hook' ) ) {
		wp_unschedule_hook( 'npcwoods_cw_batch' );
	}
	set_transient( 'npcwoods_cw_banned_at', time(), 2 * HOUR_IN_SECONDS );
	wp_schedule_single_event( time() + npcwoods_cw_delay(), 'npcwoods_cw_batch', array( 0 ) );
	npcwoods_cw_log( 'scheduled walk (' . $why . ')' );
}

add_action(
	'wpaas_cache_banned',
	function () {
		npcwoods_cw_schedule( 'wpaas_cache_banned' );
	},
	20
);

/** Home + every <loc> in the page and post sitemaps, same host only. */
function npcwoods_cw_collect_urls() {
	$urls = array( home_url( '/' ) );
	foreach ( array( 'page-sitemap.xml', 'post-sitemap.xml' ) as $map ) {
		$res = wp_remote_get(
			home_url( '/' . $map ),
			array(
				'timeout'    => 30,
				'user-agent' => 'Mozilla/5.0 (compatible; NPCWoods-CacheWarm/1.1; +https://npcwoods.com/)',
			)
		);
		if ( is_wp_error( $res ) || 200 !== (int) wp_remote_retrieve_response_code( $res ) ) {
			continue;
		}
		if ( preg_match_all( '#<loc>\s*([^<\s]+)\s*</loc>#', (string) wp_remote_retrieve_body( $res ), $m ) ) {
			$urls = array_merge( $urls, $m[1] );
		}
	}
	$host = wp_parse_url( home_url(), PHP_URL_HOST );
	$keep = array();
	foreach ( $urls as $u ) {
		$u = html_entity_decode( $u );
		if ( wp_parse_url( $u, PHP_URL_HOST ) === $host && false === strpos( $u, '?' ) ) {
			$keep[ $u ] = true;
		}
	}
	return array_keys( $keep );
}

/** One cron run: warm up to batch_size URLs from $offset within the time cap. */
function npcwoods_cw_run_batch( $offset = 0 ) {
	$offset = max( 0, (int) $offset );

	// Never let two runs overlap (a late cron tick + a rescheduled one).
	if ( get_transient( 'npcwoods_cw_lock' ) ) {
		npcwoods_cw_log( sprintf( 'batch at %d skipped: another run holds the lock', $offset ) );
		return;
	}
	set_transient( 'npcwoods_cw_lock', 1, npcwoods_cw_time_cap() + 60 );
	$started  = microtime( true );
	$run_from = time();

	$urls = ( 0 === $offset ) ? false : get_transient( 'npcwoods_cw_urls' );
	if ( ! is_array( $urls ) ) {
		$urls   = npcwoods_cw_collect_urls();
		$offset = 0;
		set_transient( 'npcwoods_cw_urls', $urls, 2 * HOUR_IN_SECONDS );
		set_transient( 'npcwoods_cw_requeued', array(), 2 * HOUR_IN_SECONDS );
	}
	$requeued = get_transient( 'npcwoods_cw_requeued' );
	if ( ! is_array( $requeued ) ) {
		$requeued = array();
	}

	$total    = count( $urls );
	$limit    = min( $total, $offset + npcwoods_cw_batch_size() );
	$cap      = npcwoods_cw_time_cap();
	$stats    = array();
	$strikes  = 0;
	$fails    = 0;
	$i        = $offset;
	$stop_why = '';

	while ( $i < $limit ) {
		if ( microtime( true ) - $started > $cap ) {
			$stop_why = 'time cap';
			break;
		}
		$u    = $urls[ $i ];
		$res  = wp_remote_get(
			$u,
			array(
				'timeout'     => npcwoods_cw_timeout(),
				'redirection' => 0,
				'user-agent'  => 'Mozilla/5.0 (compatible; NPCWoods-CacheWarm/1.1; +https://npcwoods.com/)',
			)
		);
		$code = is_wp_error( $res ) ? 0 : (int) wp_remote_retrieve_response_code( $res );
		$cf   = is_wp_error( $res ) ? '-' : (string) wp_remote_retrieve_header( $res, 'cf-cache-status' );
		$key  = $code . '/' . ( '' === $cf ? '-' : $cf );
		$stats[ $key ] = isset( $stats[ $key ] ) ? $stats[ $key ] + 1 : 1;
		$i++;

		if ( 0 === $code || $code >= 500 ) {
			// Timeout or gateway 503: re-queue this URL once at the end, back off, keep going.
			$fails++;
			$strikes++;
			if ( empty( $requeued[ $u ] ) ) {
				$requeued[ $u ] = true;
				$urls[]         = $u;
				$total          = count( $urls );
			}
			if ( $strikes >= npcwoods_cw_max_strikes() ) {
				$stop_why = 'gateway busy';
				break;
			}
			$sleep = npcwoods_cw_backoff( $strikes );
			if ( microtime( true ) - $started + $sleep > $cap ) {
				$stop_why = 'time cap';
				break;
			}
			sleep( $sleep );
		} else {
			$strikes = 0;
			usleep( npcwoods_cw_pause_us() );
		}
	}

	set_transient( 'npcwoods_cw_urls', $urls, 2 * HOUR_IN_SECONDS );
	set_transient( 'npcwoods_cw_requeued', $requeued, 2 * HOUR_IN_SECONDS );

	$parts = array();
	foreach ( $stats as $k => $n ) {
		$parts[] = $k . '=' . $n;
	}
	npcwoods_cw_log(
		sprintf(
			'batch %d-%d of %d in %ds: %s%s',
			$offset,
			$i,
			$total,
			(int) round( microtime( true ) - $started ),
			implode( ' ', $parts ),
			( '' !== $stop_why ? ' [stopped: ' . $stop_why . ']' : '' ) . ( $fails ? ' [fails ' . $fails . ']' : '' )
		)
	);

	delete_transient( 'npcwoods_cw_lock' );

	$banned_at = (int) get_transient( 'npcwoods_cw_banned_at' );
	if ( $banned_at >= $run_from ) {
		// A newer ban landed mid-run and already scheduled a fresh walk from 0.
		npcwoods_cw_log( 'newer ban during run; leaving the fresh walk to restart' );
	} elseif ( $i < $total ) {
		$gap = ( 'gateway busy' === $stop_why ) ? 120 : npcwoods_cw_batch_gap();
		wp_schedule_single_event( time() + $gap, 'npcwoods_cw_batch', array( $i ) );
	} else {
		delete_transient( 'npcwoods_cw_requeued' );
		npcwoods_cw_log( 'walk complete' );
	}
}

add_action( 'npcwoods_cw_batch', 'npcwoods_cw_run_batch', 10, 1 );
