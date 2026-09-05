<?php
/**
 * Plugin Name: NPCWoods Dental Landing Pages
 * Description: Serves standalone HTML for dental condition-specific landing pages, bypassing the theme.
 */
add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    $path_map = array(
        '/dental-pain/'              => 'dental-pain/index.html',
        '/dental-pain/search-safe/' => 'dental-pain/search-safe/index.html',
        '/dental-pain/gainesville-ga/' => 'dental-pain/gainesville-ga/index.html',
        '/dental-pain/ames-ia/'      => 'dental-pain/ames-ia/index.html',
        '/dental-pain/iowa-city-ia/' => 'dental-pain/iowa-city-ia/index.html',
        '/dental-pain/dubuque-ia/'   => 'dental-pain/dubuque-ia/index.html',
        '/dental-pain/waterloo-ia/'  => 'dental-pain/waterloo-ia/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } else {
        $slug_map = array(
            'dental-pain'    => 'dental-pain/index.html',
            'gainesville-ga' => 'dental-pain/gainesville-ga/index.html',
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
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
