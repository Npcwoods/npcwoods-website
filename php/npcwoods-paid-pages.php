<?php
/**
 * Plugin Name: NPCWoods Paid Landing Pages
 * Description: Serves noindex static HTML for paid-traffic-only landing pages (Google Ads, Facebook Ads).
 *              Separate from npcwoods-llmseo-pages.php so the entire paid surface has one kill switch.
 *              All routes here are noindex by meta tag; sitemap exclusion lives in npcwoods-faq-schema.php.
 * Version: 1.0.0
 * Author: Chris Woods / NPCWoods
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    $path_map = array(
        '/uti-care/' => 'uti-care/index.html',
        '/online-urgent-care-info/' => 'online-urgent-care-info/index.html',
        '/online-urgent-care-info/search-safe/' => 'online-urgent-care-info/search-safe/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } else {
        $slug_map = array(
            'uti-care' => 'uti-care/index.html',
        );
        $slug = get_post_field( 'post_name', get_queried_object_id() );
        if ( is_page() && isset( $slug_map[ $slug ] ) ) {
            $html_rel = $slug_map[ $slug ];
        }
    }

    if ( $html_rel ) {
        $html_file = ABSPATH . $html_rel;
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
            header( 'X-Content-Type-Options: nosniff' );
            header( 'X-Frame-Options: SAMEORIGIN' );
            header( 'Referrer-Policy: strict-origin-when-cross-origin' );
            // X-Robots-Tag belt-and-suspenders alongside the page's noindex meta tag.
            header( 'X-Robots-Tag: noindex, follow' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
