<?php
/**
 * Plugin Name: NPCWoods Security Headers
 * Description: Adds HTTPS enforcement and security headers for all WordPress-rendered pages.
 *              Static HTML bypass pages (education, experience, dental, pharmacy) need their
 *              own headers added in their respective mu-plugins.
 * Version: 1.0
 * Author: NPCWoods
 */

// Force HTTPS redirect (safety net — primary enforcement should be at Cloudflare/GoDaddy level)
add_action( 'template_redirect', function() {
    if ( ! is_ssl() && ! is_admin() ) {
        $redirect_url = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
        wp_redirect( $redirect_url, 301 );
        exit;
    }
}, 0 );

// Security headers on every WordPress response
add_action( 'send_headers', function() {
    header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );
}, 1 );
