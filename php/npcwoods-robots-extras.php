<?php
/**
 * Plugin Name: NPCWoods Robots.txt Extras
 * Description: Generates a focused robots.txt. Excludes noise directories and points
 *              crawlers (search + AI) at /llms.txt and /llms-full.txt for narrative
 *              context. Replaces Yoast's default output via the robots_txt filter.
 * Version:     3.1.0
 * Author:      NPCWoods
 *
 * 2026-05-11 — Collapsed from per-bot blocks (v2.0.0) to a single User-agent: * block.
 * Every AI crawler in the previous version had identical rules (Allow: / + same Disallows),
 * so the global block covers them all by default. Net change: ~150 lines → ~20 lines, no
 * functional difference. AI welcome message kept as a comment header.
 *
 * 2026-09-03 — Register /llms-sitemap.xml in the Yoast index and page sitemap so
 * naive crawlers that never read robots.txt comments still find /llms.txt and
 * /llms-full.txt. Those files stay noindex (no canonical). robots.txt already
 * points at /sitemap_index.xml; /sitemap.xml is a 301, not a 404.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'robots_txt', function ( $robots_txt, $public ) {
	// Respect the site-wide "discourage indexing" toggle — fall through to Yoast's default.
	if ( '0' === (string) $public ) {
		return $robots_txt;
	}

	$disallows = array(
		'/automation-output/',
		'/backups/',
		'/scripts/',
		'/*.bak',
		'/*.meta-bak',
		'/*.synced.bak',
	);

	$output  = "# NPCWoods.com — Async telemedicine by Chris Woods, MSN, APRN, FNP-C\n";
	$output .= "# Licensed Nurse Practitioner — 11 states (AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT)\n";
	$output .= "# NPI: 1285125468 — https://npiregistry.cms.hhs.gov/\n";
	$output .= "#\n";
	$output .= "# Context for AI assistants and search crawlers:\n";
	$output .= "#   /llms.txt       — short reference (pages, services, credentials)\n";
	$output .= "#   /llms-full.txt  — full reference (conditions, medications, clinical guidelines)\n";
	$output .= "#\n";
	$output .= "# All crawlers welcome (GPTBot, Google-Extended, ClaudeBot, PerplexityBot,\n";
	$output .= "# Applebot-Extended, CCBot, Bytespider, FacebookBot, Amazonbot, Grok, and others).\n";
	$output .= "# Rules below apply to every user-agent.\n\n";

	$output .= "User-agent: *\n";
	foreach ( $disallows as $rule ) {
		$output .= "Disallow: {$rule}\n";
	}
	$output .= "\n";

	$output .= "# /sitemap.xml 301s here. That 301 is the real sitemap, not a missing file.\n";
	$output .= "Sitemap: https://npcwoods.com/sitemap_index.xml\n";

	return $output;
}, PHP_INT_MAX, 2 );

/**
 * Lastmod for the AI reference files. Uses the web-root llms.txt mtime when
 * the file is readable; otherwise the locked copy date in the file header.
 */
function npcwoods_llms_sitemap_lastmod() {
	$file = ABSPATH . 'llms.txt';
	if ( is_readable( $file ) ) {
		return gmdate( 'c', filemtime( $file ) );
	}
	return '2026-09-01T00:00:00+00:00';
}

function npcwoods_llms_sitemap_urls() {
	return array(
		'https://npcwoods.com/llms.txt',
		'https://npcwoods.com/llms-full.txt',
	);
}

function npcwoods_llms_urlset_xml() {
	$lastmod = npcwoods_llms_sitemap_lastmod();
	$xml     = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
	foreach ( npcwoods_llms_sitemap_urls() as $url ) {
		$xml .= "\t<url>\n";
		$xml .= "\t\t<loc>" . esc_url( $url ) . "</loc>\n";
		$xml .= "\t\t<lastmod>" . esc_html( $lastmod ) . "</lastmod>\n";
		$xml .= "\t</url>\n";
	}
	$xml .= '</urlset>';
	return $xml;
}

// Yoast rewrite already sends *-sitemap.xml to WordPress. Serve the body
// ourselves so www and apex both get 200 even if Yoast never registered
// an "llms" sitemap type.
add_action( 'init', function () {
	$path = parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH );
	if ( $path !== '/llms-sitemap.xml' && $path !== '/llms-sitemap.xml/' ) {
		return;
	}
	status_header( 200 );
	header( 'Content-Type: text/xml; charset=UTF-8' );
	header( 'X-Robots-Tag: noindex, follow' );
	echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
	echo npcwoods_llms_urlset_xml();
	exit;
}, 1 );

// List the dedicated sitemap in Yoast's index so crawlers that only follow
// sitemap_index.xml still find the AI reference files.
add_filter( 'wpseo_sitemap_index', function ( $extra ) {
	$loc     = 'https://npcwoods.com/llms-sitemap.xml';
	$lastmod = npcwoods_llms_sitemap_lastmod();
	$extra  .= '<sitemap>';
	$extra  .= '<loc>' . esc_url( $loc ) . '</loc>';
	$extra  .= '<lastmod>' . esc_html( $lastmod ) . '</lastmod>';
	$extra  .= '</sitemap>';
	return $extra;
} );

// Naive checkers that only parse page-sitemap.xml never see robots comments.
// Append the same two URLs there too. Do not add a canonical — these files
// are crawler references, not ranking pages.
add_filter( 'wpseo_sitemap_page_content', function ( $content ) {
	$lastmod = npcwoods_llms_sitemap_lastmod();
	foreach ( npcwoods_llms_sitemap_urls() as $url ) {
		$content .= '<url>';
		$content .= '<loc>' . esc_url( $url ) . '</loc>';
		$content .= '<lastmod>' . esc_html( $lastmod ) . '</lastmod>';
		$content .= '</url>';
	}
	return $content;
} );
