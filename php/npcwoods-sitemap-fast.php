<?php
/**
 * Plugin Name: NPCWoods Sitemap Fast Path
 * Description: Warms Yoast sitemap XML to static files and serves them early so
 *              post-sitemap.xml / page-sitemap.xml / sitemap_index.xml avoid
 *              GoDaddy gateway soft-503 under parallel load. Does not delete posts.
 * Version: 1.0.0
 * Author: NPCWoods
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Cache TTL for warm sitemap files (seconds). */
const NPCWOODS_SITEMAP_CACHE_TTL = 43200; // 12 hours

/**
 * @return array<string,string> request path => filename
 */
function npcwoods_sitemap_fast_targets() {
	return array(
		'/sitemap_index.xml' => 'sitemap_index.xml',
		'/post-sitemap.xml'  => 'post-sitemap.xml',
		'/page-sitemap.xml'  => 'page-sitemap.xml',
	);
}

function npcwoods_sitemap_fast_cache_dir() {
	$dir = WP_CONTENT_DIR . '/cache/npcwoods-sitemaps';
	if ( ! is_dir( $dir ) ) {
		if ( function_exists( 'wp_mkdir_p' ) ) {
			wp_mkdir_p( $dir );
		} else {
			@mkdir( $dir, 0755, true );
		}
	}
	return $dir;
}

function npcwoods_sitemap_fast_candidates( $filename ) {
	return array(
		npcwoods_sitemap_fast_cache_dir() . '/' . $filename,
		ABSPATH . $filename,
	);
}

function npcwoods_sitemap_fast_fresh_file( $filename ) {
	foreach ( npcwoods_sitemap_fast_candidates( $filename ) as $candidate ) {
		if ( is_readable( $candidate ) && ( time() - (int) filemtime( $candidate ) ) < NPCWOODS_SITEMAP_CACHE_TTL ) {
			return $candidate;
		}
	}
	return '';
}

function npcwoods_sitemap_fast_write( $filename, $xml ) {
	if ( ! is_string( $xml ) || $xml === '' ) {
		return;
	}
	if ( strpos( $xml, '<urlset' ) === false && strpos( $xml, '<sitemapindex' ) === false ) {
		return;
	}
	$dir = npcwoods_sitemap_fast_cache_dir();
	$cache_file = $dir . '/' . $filename;
	@file_put_contents( $cache_file, $xml );
	// Physical file at web root: nginx try_files can serve without PHP.
	@file_put_contents( ABSPATH . $filename, $xml );
}

function npcwoods_sitemap_fast_invalidate() {
	foreach ( npcwoods_sitemap_fast_targets() as $filename ) {
		foreach ( npcwoods_sitemap_fast_candidates( $filename ) as $candidate ) {
			if ( is_file( $candidate ) ) {
				@unlink( $candidate );
			}
		}
	}
}

// Trim image bloat on rebuild (pages stay; images in post sitemap are optional).
add_filter( 'wpseo_xml_sitemap_img', '__return_false' );

// Serve warm copy before Yoast rebuilds (init priority 0).
add_action(
	'init',
	function () {
		if ( is_admin() ) {
			return;
		}
		$path = parse_url( isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '', PHP_URL_PATH );
		$targets = npcwoods_sitemap_fast_targets();
		if ( ! is_string( $path ) || ! isset( $targets[ $path ] ) ) {
			return;
		}
		$filename = $targets[ $path ];
		$fresh = npcwoods_sitemap_fast_fresh_file( $filename );
		if ( $fresh ) {
			header( 'Content-Type: text/xml; charset=UTF-8' );
			header( 'X-Robots-Tag: noindex, follow' );
			header( 'Cache-Control: public, max-age=3600, s-maxage=86400' );
			header( 'X-NPCWoods-Sitemap: cache' );
			readfile( $fresh );
			exit;
		}
		// Miss: let Yoast generate, capture body, warm cache for next hit.
		ob_start(
			function ( $xml ) use ( $filename ) {
				npcwoods_sitemap_fast_write( $filename, $xml );
				return $xml;
			}
		);
	},
	0
);

// Drop warm files when content that affects sitemaps changes.
add_action(
	'save_post',
	function ( $post_id ) {
		if ( wp_is_post_revision( $post_id ) || ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) ) {
			return;
		}
		$status = get_post_status( $post_id );
		if ( ! in_array( $status, array( 'publish', 'trash', 'private', 'draft' ), true ) ) {
			return;
		}
		npcwoods_sitemap_fast_invalidate();
	},
	20
);

add_action(
	'deleted_post',
	function () {
		npcwoods_sitemap_fast_invalidate();
	},
	20
);
