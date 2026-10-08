<?php
/**
 * Plugin Name: NPCWoods Cache Warm
 * Description: GoDaddy WPaaS bans the whole page cache (gateway + CDN) on every
 *              publish/update. Until pages are re-cached, every crawler request
 *              goes through the GoDaddy gateway rate limiter
 *              (x-gateway-rate-limit-delayed), which queues bursts ~20s and then
 *              answers 503. This re-warms the CDN copy of every sitemap URL in
 *              small, slow WP-cron batches a few minutes after each ban, so
 *              Googlebot gets cached 200s instead of 503s. Read-only GETs only.
 * Version: 1.0.0
 * Author: NPCWoods
 *
 * Kitchen source: php/npcwoods-cache-warm.php (2026-10-08 crawl fixes).
 * Kill switch: delete this file. All functions are prefixed npcwoods_cw_.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Seconds to wait after a ban before warming (lets the CDN purge finish). */
function npcwoods_cw_delay() {
	return 240;
}

/** URLs per cron batch, pause between GETs (microseconds), gap between batches. */
function npcwoods_cw_batch_size() {
	return 15;
}
function npcwoods_cw_pause_us() {
	return 700000;
}
function npcwoods_cw_batch_gap() {
	return 20;
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
				'user-agent' => 'Mozilla/5.0 (compatible; NPCWoods-CacheWarm/1.0; +https://npcwoods.com/)',
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

add_action(
	'npcwoods_cw_batch',
	function ( $offset = 0 ) {
		$offset = max( 0, (int) $offset );
		$urls   = ( 0 === $offset ) ? false : get_transient( 'npcwoods_cw_urls' );
		if ( ! is_array( $urls ) ) {
			$urls = npcwoods_cw_collect_urls();
			set_transient( 'npcwoods_cw_urls', $urls, 2 * HOUR_IN_SECONDS );
			$offset = 0;
		}
		$total   = count( $urls );
		$batch   = array_slice( $urls, $offset, npcwoods_cw_batch_size() );
		$started = microtime( true );
		$done    = 0;
		$stats   = array();
		$strikes = 0;
		foreach ( $batch as $u ) {
			if ( microtime( true ) - $started > 60 ) {
				break;
			}
			$res  = wp_remote_get(
				$u,
				array(
					'timeout'     => 12,
					'redirection' => 0,
					'user-agent'  => 'Mozilla/5.0 (compatible; NPCWoods-CacheWarm/1.0; +https://npcwoods.com/)',
				)
			);
			$code = is_wp_error( $res ) ? 0 : (int) wp_remote_retrieve_response_code( $res );
			$cf   = is_wp_error( $res ) ? '-' : (string) wp_remote_retrieve_header( $res, 'cf-cache-status' );
			$key  = $code . '/' . ( '' === $cf ? '-' : $cf );
			$stats[ $key ] = isset( $stats[ $key ] ) ? $stats[ $key ] + 1 : 1;
			$done++;
			$strikes = ( 0 === $code || $code >= 500 ) ? $strikes + 1 : 0;
			if ( $strikes >= 3 ) {
				break; // Gateway is busy; back off and resume later.
			}
			usleep( npcwoods_cw_pause_us() );
		}
		$next = $offset + $done;
		$parts = array();
		foreach ( $stats as $k => $n ) {
			$parts[] = $k . '=' . $n;
		}
		npcwoods_cw_log( sprintf( 'batch %d-%d of %d: %s', $offset, $next, $total, implode( ' ', $parts ) ) );
		if ( $next < $total ) {
			$gap = ( $strikes >= 3 ) ? 120 : npcwoods_cw_batch_gap();
			wp_schedule_single_event( time() + $gap, 'npcwoods_cw_batch', array( $next ) );
		} else {
			npcwoods_cw_log( 'walk complete' );
		}
	},
	10,
	1
);
