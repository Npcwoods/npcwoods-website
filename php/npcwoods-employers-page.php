<?php
/**
 * Plugin Name: NPCWoods Employers Page
 * Description: Serves the static /employers/ landing page (employer health, $59 text visits) from html/employers/index.html, bypassing the theme.
 * Version: 1.0
 * Author: NPCWoods
 *
 * Single route, anonymous closure only (no named functions), so it cannot
 * collide with any other mu-plugin.
 */
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'template_redirect', function () {
    if ( ! is_page() ) {
        return;
    }
    $slug = get_post_field( 'post_name', get_queried_object_id() );
    if ( 'employers' !== $slug ) {
        return;
    }
    $html_file = ABSPATH . 'employers/index.html';
    if ( ! file_exists( $html_file ) ) {
        return;
    }
    header( 'Content-Type: text/html; charset=UTF-8' );
    header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );
    readfile( $html_file );
    exit;
}, 1 );
