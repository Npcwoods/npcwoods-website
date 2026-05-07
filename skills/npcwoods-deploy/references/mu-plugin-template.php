<?php
/**
 * Plugin Name: NPCWoods [SECTION_NAME] Pages
 * Description: Serves standalone HTML for [SECTION_NAME] pages, bypassing the theme.
 * Version: 1.0
 * Author: NPCWoods
 *
 * INSTALLATION:
 * 1. Upload this file to: /wp-content/mu-plugins/npcwoods-[section]-pages.php
 * 2. Upload HTML files to their matching paths under the web root
 * 3. Create WordPress page stubs at each slug via REST API
 *
 * PATTERN EXPLANATION:
 * - is_page() only returns true when a WordPress page exists at the slug
 * - get_post_field('post_name', ...) gets the slug of the current page
 * - We check the slug against our map and serve the static HTML if it matches
 * - Priority 1 ensures this runs before other template_redirect hooks
 * - ABSPATH resolves to the web root (html/) on GoDaddy
 *
 * DO NOT USE:
 * - $_SERVER['REQUEST_URI'] matching (nginx 404s before PHP runs)
 * - 'init' hook (same nginx issue — page must exist in WP first)
 */

add_action( 'template_redirect', function() {
    // Map page slugs → static HTML file paths (relative to ABSPATH / web root)
    $page_map = array(
        // 'page-slug'    => 'section/page-slug/index.html',
        // 'another-slug' => 'section/another-slug/index.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
