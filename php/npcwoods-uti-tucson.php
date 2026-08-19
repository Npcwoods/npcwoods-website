<?php
/**
 * Plugin Name: NPCWoods UTI Tucson
 * Description: Serves standalone HTML for /uti-treatment/tucson-az/ only.
 */
add_action( 'template_redirect', function() {
    $page_map = array(
        '/uti-treatment/tucson-az/' => 'uti-treatment/tucson-az/index.html',
    );

    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    if ( is_page() && isset( $page_map[ $path ] ) ) {
        $html_file = ABSPATH . $page_map[ $path ];
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
