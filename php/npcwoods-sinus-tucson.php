<?php
/**
 * Plugin Name: NPCWoods Sinus Tucson
 * Description: Serves standalone HTML for /sinus-infection-treatment/tucson-az/ only.
 */
add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    if ( is_page() && $path === '/sinus-infection-treatment/tucson-az/' ) {
        $html_file = ABSPATH . 'sinus-infection-treatment/tucson-az/index.html';
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
