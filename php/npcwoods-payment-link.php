<?php
/**
 * Plugin Name: NPCWoods Payment Link
 * Description: Serves /pay/ as a noindex browser redirect to Stripe with safe attribution labels.
 */

add_action( 'template_redirect', function() {
    if ( ! is_page() ) {
        return;
    }

    $slug = get_post_field( 'post_name', get_queried_object_id() );
    if ( 'pay' !== $slug ) {
        return;
    }

    nocache_headers();
    header( 'Content-Type: text/html; charset=UTF-8', true );
    header( 'X-Robots-Tag: noindex, nofollow', true );
    header( 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0', true );
    header( 'Surrogate-Control: no-store', true );
    header( 'Pragma: no-cache', true );

    $html_file = ABSPATH . 'landing-pages/pay/index.html';
    if ( file_exists( $html_file ) ) {
        readfile( $html_file );
        exit;
    }
    wp_die( 'Payment page configuration is missing.', 'Error', array( 'response' => 404 ) );
}, 1 );
