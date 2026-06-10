<?php
/**
 * Plugin Name: NPCWoods GLP-1 Pages
 * Description: Serves standalone HTML for GLP-1 weight loss pages, bypassing the theme.
 */

add_action( 'template_redirect', function() {
    $page_map = array(
        'glp1-weight-loss' => 'glp1-weight-loss/index.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
