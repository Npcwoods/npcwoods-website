<?php
/**
 * Plugin Name: NPCWoods GA/NC City Pages
 * Description: Serves standalone HTML for GA and NC city landing pages.
 */
add_action( 'template_redirect', function() {
    $page_map = array(
        'murphy-nc'     => 'murphy-nc/index.html',
        'blairsville-ga'=> 'blairsville-ga/index.html',
        'blue-ridge-ga' => 'blue-ridge-ga/index.html',
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
