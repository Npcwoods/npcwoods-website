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
    $page_map = array(
        // Paid clone of /uti-treatment/ — only paid Google or Facebook traffic should land here.
        'uti-care' => 'uti-care/index.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
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
