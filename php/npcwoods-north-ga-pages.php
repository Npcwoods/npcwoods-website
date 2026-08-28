<?php
/**
 * Plugin Name: NPCWoods North GA Pages
 * Description: Serves standalone HTML for Woodstock / Marietta / Canton / Cherokee plates.
 */
add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    // Path map wins over WP slug so /uti-treatment/canton-ga/ is the city door,
    // not a redirect onto the listicle at /canton-ga-urgent-care-text-visit/.
    $path_map = array(
        '/uti-treatment/woodstock-ga/' => 'uti-treatment/woodstock-ga/index.html',
        '/uti-treatment/canton-ga/'    => 'uti-treatment/canton-ga/index.html',
    );

    $page_map = array(
        'woodstock-ga'                         => 'uti-treatment/woodstock-ga/index.html',
        'skip-the-urgent-care-woodstock-ga'    => 'skip-the-urgent-care-woodstock-ga/index.html',
        'urgent-care-vs-text-visit-cobb-county'=> 'urgent-care-vs-text-visit-cobb-county/index.html',
        'canton-ga'                            => 'uti-treatment/canton-ga/index.html',
        'canton-ga-urgent-care-text-visit'     => 'canton-ga-urgent-care-text-visit/index.html',
        'urgent-care-line-marietta-ga'         => 'urgent-care-line-marietta-ga/index.html',
        'urgent-care-near-me-cherokee-county'  => 'urgent-care-near-me-cherokee-county/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } elseif ( is_page() ) {
        $slug = get_post_field( 'post_name', get_queried_object_id() );
        if ( isset( $page_map[ $slug ] ) ) {
            $html_rel = $page_map[ $slug ];
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
