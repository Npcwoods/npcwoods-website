<?php
/**
 * Plugin Name: NPCWoods UTI Mix Wave Week 1
 * Description: Serves standalone HTML for Savannah, Raleigh, Denver, and Las Vegas UTI city pages.
 */
add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    $path_map = array(
        '/uti-treatment/savannah-ga/'   => 'uti-treatment/savannah-ga/index.html',
        '/uti-treatment/raleigh-nc/'    => 'uti-treatment/raleigh-nc/index.html',
        '/uti-treatment/denver-co/'     => 'uti-treatment/denver-co/index.html',
        '/uti-treatment/las-vegas-nv/'  => 'uti-treatment/las-vegas-nv/index.html',
    );

    if ( isset( $path_map[ $path ] ) ) {
        $html_file = ABSPATH . $path_map[ $path ];
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
