<?php
/**
 * Plugin Name: NPCWoods UTI Charlotte
 * Description: Serves standalone HTML for /uti-treatment/charlotte-nc/ only.
 */
add_action( 'template_redirect', function() {
    $page_map = array(
        '/uti-treatment/charlotte-nc/' => 'uti-treatment/charlotte-nc/index.html',
    );

    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    if ( isset( $page_map[ $path ] ) ) {
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
