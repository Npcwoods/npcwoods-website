<?php
/**
 * Plugin Name: NPCWoods GLP-1 Pages
 * Description: Serves standalone HTML for GLP-1 weight loss and /learn/glp1/ explainer pages, bypassing the theme.
 */

add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    $path_map = array(
        '/glp1-weight-loss/'              => 'glp1-weight-loss/index.html',
        '/learn/glp1/'                    => 'learn/glp1/index.html',
        '/learn/glp1/how-they-work/'      => 'learn/glp1/how-they-work/index.html',
        '/learn/glp1/side-effects/'       => 'learn/glp1/side-effects/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } else {
        $slug_map = array(
            'glp1-weight-loss' => 'glp1-weight-loss/index.html',
            'glp1'             => 'learn/glp1/index.html',
            'how-they-work'    => 'learn/glp1/how-they-work/index.html',
            'side-effects'     => 'learn/glp1/side-effects/index.html',
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
            header( 'X-NPCWoods-Page: glp1' );
            header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
            header( 'X-Content-Type-Options: nosniff' );
            header( 'X-Frame-Options: SAMEORIGIN' );
            header( 'Referrer-Policy: strict-origin-when-cross-origin' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
