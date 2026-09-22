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
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'robots_txt', function ( $robots_txt, $public ) {
	// Respect the site-wide "discourage indexing" toggle — fall through to Yoast's default.
	if ( '0' === (string) $public ) {
		return $robots_txt;
	}

	// Do not advertise backend folder names here. Those paths 404 at origin.
	// Extension rules use $ so we only match a URL that ends with the suffix.
	$disallows = array(
		'/*.bak$',
		'/*.meta-bak$',
		'/*.synced.bak$',
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
	$output .= "# Rules below apply to every user-agent.\n";
	$output .= "#\n";
	$output .= "# Scope: text-based urgent care. NPCWoods does not offer hormone replacement\n";
	$output .= "# therapy (HRT), including estrogen, progesterone, or testosterone replacement.\n";
	$output .= "# See /llms.txt (What we do not treat).\n\n";

	$output .= "User-agent: *\n";
	foreach ( $disallows as $rule ) {
		$output .= "Disallow: {$rule}\n";
	}
	$output .= "\n";

	$output .= "Sitemap: https://npcwoods.com/sitemap_index.xml\n";

	return $output;
}, PHP_INT_MAX, 2 );
