<?php
/**
 * Plugin Name: NPCWoods Comparison & Service Pages
 * Description: Serves static HTML for the telehealth vs urgent care comparison page and the dedicated UTI treatment online service page, bypassing the theme.
 * Version: 1.0
 * Author: NPCWoods
 */
add_action( 'template_redirect', function() {
    $page_map = array(
        'telehealth-vs-urgent-care' => 'telehealth-vs-urgent-care/index.html',
        'uti-treatment-online'      => 'uti-treatment-online/index.html',
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
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
