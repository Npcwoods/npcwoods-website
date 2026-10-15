<?php
/**
 * Plugin Name: NPCWoods Sinus Las Vegas
 * Description: Serves standalone HTML for /sinus-infection-treatment/las-vegas-nv/ only.
 *              Also stops WordPress redirect_canonical from sending this path
 *              to /uti-treatment/las-vegas-nv/ (same city slug, different parent).
 */
add_filter( 'redirect_canonical', function( $redirect_url ) {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( (string) $path );
    if ( $path === '/sinus-infection-treatment/las-vegas-nv/' ) {
        return false;
    }
    return $redirect_url;
} );

add_action( 'template_redirect', function() {
    $page_map = array(
        '/sinus-infection-treatment/las-vegas-nv/' => 'sinus-infection-treatment/las-vegas-nv/index.html',
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
