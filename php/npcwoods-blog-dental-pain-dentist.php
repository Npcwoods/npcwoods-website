<?php
/**
 * Plugin Name: NPCWoods Blog Dental Pain No Dentist
 * Description: Serves standalone HTML for /blog/dental-pain-cant-get-a-dentist/ only.
 */
add_action( 'template_redirect', function() {
    $page_map = array(
        '/blog/dental-pain-cant-get-a-dentist/' => 'blog/dental-pain-cant-get-a-dentist/index.html',
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
