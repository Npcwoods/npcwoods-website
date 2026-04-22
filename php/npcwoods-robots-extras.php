<?php
/**
 * Plugin Name: NPCWoods Robots.txt Extras
 * Description: Generates a complete robots.txt that explicitly welcomes the major AI
 *              crawlers (ChatGPT, Gemini, Claude, Perplexity, Grok, and others) and
 *              excludes noise directories. Links to /llms.txt and /llms-full.txt for
 *              narrative context. Replaces Yoast's default output via the robots_txt
 *              filter — returns the full file rather than appending.
 * Version:     2.0.0
 * Author:      NPCWoods
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

	// Grouped by vendor. Label => list of user-agent strings.
	$ai_bots = array(
		'OpenAI / ChatGPT'                        => array( 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User' ),
		'Google (Gemini / Vertex / AI Overviews)' => array( 'Google-Extended', 'GoogleOther' ),
		'Anthropic / Claude'                      => array( 'ClaudeBot', 'Claude-Web', 'anthropic-ai' ),
		'Perplexity'                              => array( 'PerplexityBot', 'Perplexity-User' ),
		'xAI / Grok'                              => array( 'Grok', 'GrokBot', 'xAI-Bot', 'xAI-Grok', 'Grok-DeepSearch' ),
		'Apple Intelligence'                      => array( 'Applebot-Extended' ),
		'Common Crawl (LLM training)'             => array( 'CCBot' ),
		'Meta AI'                                 => array( 'FacebookBot', 'meta-externalagent' ),
		'Amazon'                                  => array( 'Amazonbot' ),
		'ByteDance / TikTok / Doubao'             => array( 'Bytespider' ),
	);

	$output  = "# NPCWoods.com — Async telemedicine by Chris Woods, MSN, APRN, FNP-C\n";
	$output .= "# Licensed Nurse Practitioner — 11 states (AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT)\n";
	$output .= "# NPI: 1285125468 — https://npiregistry.cms.hhs.gov/\n";
	$output .= "#\n";
	$output .= "# Context for AI assistants:\n";
	$output .= "#   /llms.txt       — short reference (pages, services, credentials)\n";
	$output .= "#   /llms-full.txt  — full reference (conditions, medications, clinical guidelines)\n";
	$output .= "#\n";
	$output .= "# All major AI crawlers are explicitly welcomed below.\n\n";

	$output .= "User-agent: *\n";
	foreach ( $disallows as $rule ) {
		$output .= "Disallow: {$rule}\n";
	}
	$output .= "\n";

	foreach ( $ai_bots as $label => $agents ) {
		$output .= "# ===== {$label} =====\n";
		foreach ( $agents as $agent ) {
			$output .= "User-agent: {$agent}\n";
			$output .= "Allow: /\n";
			foreach ( $disallows as $rule ) {
				$output .= "Disallow: {$rule}\n";
			}
			$output .= "\n";
		}
	}

	$output .= "Sitemap: https://npcwoods.com/sitemap_index.xml\n";

	return $output;
}, PHP_INT_MAX, 2 );
