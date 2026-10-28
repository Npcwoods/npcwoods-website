<?php
/**
 * Plugin Name: NPCWoods Yoast Homepage Schema Off
 * Description: Stops Yoast's JSON-LD graph (yoast-schema-graph) on the homepage only.
 *              The homepage template (page-npcwoods-home.php) carries its own schema
 *              (MedicalBusiness / #chris-woods Person / WebSite). Since the Rocket move
 *              and the Yoast 28.8 update, Yoast also printed an Article/BlogPosting,
 *              a duplicate #website node and a second Chris Person without the full
 *              credential line. Every other page is untouched.
 *              Chris approved 2026-10-28 ("fix the yoast thing").
 * Closure only (no named functions) so it can never collide with another mu-plugin.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter(
	'wpseo_json_ld_output',
	static function ( $data ) {
		if ( is_front_page() ) {
			return false;
		}
		return $data;
	},
	20
);
