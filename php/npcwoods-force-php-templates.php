<?php
/**
 * Plugin Name: NPCWoods Force PHP Page Templates
 * Description: Block themes ignore PHP page templates. Force page-npcwoods-*.php when assigned.
 */

add_filter(
	'template_include',
	static function ( $template ) {
		if ( is_admin() ) {
			return $template;
		}

		$slug = get_page_template_slug();
		if ( ! is_string( $slug ) || $slug === '' || substr( $slug, -4 ) !== '.php' ) {
			return $template;
		}
		if ( strpos( $slug, 'page-npcwoods-' ) !== 0 ) {
			return $template;
		}

		$candidates = array(
			get_stylesheet_directory() . '/' . $slug,
			get_template_directory() . '/' . $slug,
			WP_CONTENT_DIR . '/themes/twentytwentyfour/' . $slug,
			WP_CONTENT_DIR . '/themes/flavor/' . $slug,
		);

		foreach ( $candidates as $path ) {
			if ( is_readable( $path ) ) {
				return $path;
			}
		}

		return $template;
	},
	99
);
