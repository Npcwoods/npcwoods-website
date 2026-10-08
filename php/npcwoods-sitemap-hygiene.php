<?php
/**
 * Plugin Name: NPCWoods Sitemap Hygiene
 * Description: (1) Drops noindex / redirecting / canonical-elsewhere WordPress
 *              objects from the Yoast sitemap (merged on top of the base list in
 *              npcwoods-faq-schema.php). (2) Adds indexable static-only pages
 *              that have no WordPress object (served by nginx from html/<path>/
 *              index.html) to page-sitemap.xml, with lastmod = file mtime.
 * Version: 1.0.0
 * Author: NPCWoods
 *
 * Kitchen source: php/npcwoods-sitemap-hygiene.php (2026-10-08 crawl fixes).
 * Functions are prefixed npcwoods_smh_. Kill switch: delete this file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** WordPress post IDs that must never be listed in the sitemap. */
function npcwoods_smh_excluded_ids() {
	return array(
		// Paid-only landers, noindex,nofollow by design (npcwoods-paid-pages.php).
		998,  // /online-urgent-care-info/
		999,  // /online-urgent-care-info/search-safe/
	);
}

/**
 * Static pages (no WP object) that belong in page-sitemap.xml.
 * path => file under ABSPATH. Each one is 200 on its clean URL, has exactly
 * one self canonical, and no noindex (checked 2026-10-08).
 */
function npcwoods_smh_static_pages() {
	return array(
		'/uti-treatment/how-fast-do-uti-antibiotics-work/' => 'uti-treatment/how-fast-do-uti-antibiotics-work/index.html',
		'/uti-treatment/is-my-uti-getting-worse/'          => 'uti-treatment/is-my-uti-getting-worse/index.html',
		'/uti-treatment/no-video-uti-treatment/'           => 'uti-treatment/no-video-uti-treatment/index.html',
		'/uti-treatment/uti-antibiotics-online/'           => 'uti-treatment/uti-antibiotics-online/index.html',
	);
}

add_filter(
	'wpseo_exclude_from_sitemap_by_post_ids',
	function ( $ids ) {
		$ids = is_array( $ids ) ? $ids : array();
		return array_values( array_unique( array_map( 'intval', array_merge( $ids, npcwoods_smh_excluded_ids() ) ) ) );
	},
	20
);

add_filter(
	'wpseo_sitemap_page_content',
	function ( $content ) {
		$content = is_string( $content ) ? $content : '';
		foreach ( npcwoods_smh_static_pages() as $path => $rel ) {
			$file = ABSPATH . $rel;
			if ( ! is_readable( $file ) ) {
				continue;
			}
			$loc = home_url( $path );
			if ( false !== strpos( $content, '<loc>' . $loc . '</loc>' ) ) {
				continue;
			}
			$html = (string) @file_get_contents( $file, false, null, 0, 20000 );
			if ( preg_match( '/<meta[^>]+name=["\']robots["\'][^>]+noindex/i', $html ) ) {
				continue;
			}
			$content .= "\t<url>\n\t\t<loc>" . esc_url( $loc ) . "</loc>\n\t\t<lastmod>"
				. gmdate( 'Y-m-d\TH:i:s+00:00', (int) filemtime( $file ) ) . "</lastmod>\n\t</url>\n";
		}
		return $content;
	}
);
