<?php
/**
 * Plugin Name: NPCWoods Paid Landing Pages
 * Description: Serves noindex static HTML for paid-traffic-only landing pages (Google Ads, Facebook Ads).
 *              Separate from npcwoods-llmseo-pages.php so the entire paid surface has one kill switch.
 *              All routes here are noindex by meta tag; sitemap exclusion lives in npcwoods-faq-schema.php.
 * Version: 1.0.0
 * Author: Chris Woods / NPCWoods
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function npcwoods_ads_click_ingest() {
    header( 'Content-Type: application/json; charset=UTF-8' );
    header( 'Cache-Control: no-store' );
    header( 'X-Robots-Tag: noindex, nofollow' );
    $raw = file_get_contents( 'php://input' );
    $data = json_decode( is_string( $raw ) ? $raw : '', true );
    if ( ! is_array( $data ) ) {
        http_response_code( 400 );
        echo '{"ok":false}';
        return;
    }
    $allowed = array( 'gclid', 'gbraid', 'wbraid', 'ref', 'ts' );
    $row = array();
    foreach ( $allowed as $key ) {
        $value = isset( $data[ $key ] ) ? (string) $data[ $key ] : '';
        $row[ $key ] = preg_replace( '/[^a-zA-Z0-9_-]/', '', substr( $value, 0, 180 ) );
    }
    $row['ts'] = preg_replace( '/[^0-9]/', '', substr( (string) ( $data['ts'] ?? '' ), 0, 20 ) );
    $log = ( defined( 'WP_CONTENT_DIR' ) ? WP_CONTENT_DIR : ( ABSPATH . 'wp-content' ) ) . '/.npc-ads-click.jsonl';
    $line = wp_json_encode( $row );
    if ( is_string( $line ) && $line !== '' ) {
        @file_put_contents( $log, $line . "\n", FILE_APPEND | LOCK_EX );
    }
    echo '{"ok":true}';
}

add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    if ( $path === '/t/click/' && ( $_SERVER['REQUEST_METHOD'] ?? '' ) === 'POST' ) {
        npcwoods_ads_click_ingest();
        exit;
    }

    $path_map = array(
        '/uti-care/' => 'uti-care/index.html',
        '/online-urgent-care-info/' => 'online-urgent-care-info/index.html',
        '/online-urgent-care-info/search-safe/' => 'online-urgent-care-info/search-safe/index.html',
        '/start-uti/' => 'start-uti/index.html',
        '/start-sinus/' => 'start-sinus/index.html',
        '/start-dental/' => 'start-dental/index.html',
        '/start-uri/' => 'start-uri/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } else {
        $slug_map = array(
            'uti-care' => 'uti-care/index.html',
            'start-uti' => 'start-uti/index.html',
            'start-sinus' => 'start-sinus/index.html',
            'start-dental' => 'start-dental/index.html',
            'start-uri' => 'start-uri/index.html',
        );
        $slug = get_post_field( 'post_name', get_queried_object_id() );
        if ( is_page() && isset( $slug_map[ $slug ] ) ) {
            $html_rel = $slug_map[ $slug ];
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
            // X-Robots-Tag belt-and-suspenders alongside the page's noindex meta tag.
            header( 'X-Robots-Tag: noindex, follow' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
