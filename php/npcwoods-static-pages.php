<?php
/**
 * Plugin Name: NPCWoods Static Pages
 * Description: Serves standalone HTML for state landing pages, conditions hub, and sitemap
 */
add_action( "template_redirect", function() {
    $page_map = array(
        "arizona-telemedicine" => "arizona-telemedicine/index.html",
        "conditions"             => "conditions/index.html",
        "sitemap"                => "sitemap/index.html",
        "uti-treatment"          => "uti-treatment/index.html",
        "sinus-infection-treatment" => "sinus-infection-treatment/index.html",
        "colorado-telemedicine"  => "colorado-telemedicine/index.html",
        "idaho-telemedicine"     => "idaho-telemedicine/index.html",
        "iowa-telemedicine"      => "iowa-telemedicine/index.html",
        "montana-telemedicine"   => "montana-telemedicine/index.html",
        "nevada-telemedicine"    => "nevada-telemedicine/index.html",
        "new-mexico-telemedicine"=> "new-mexico-telemedicine/index.html",
        "north-carolina-telemedicine" => "north-carolina-telemedicine/index.html",
        "oregon-telemedicine"    => "oregon-telemedicine/index.html",
        "utah-telemedicine"      => "utah-telemedicine/index.html",
        "ed-treatment"           => "ed-treatment/index.html",        "pricing"                    => "pricing/index.html",        "credentials"                => "credentials/index.html",


    );

    $slug = get_post_field( "post_name", get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( "Content-Type: text/html; charset=UTF-8" );
            header( "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload" );
            header( "X-Content-Type-Options: nosniff" );
            header( "X-Frame-Options: SAMEORIGIN" );
            header( "Referrer-Policy: strict-origin-when-cross-origin" );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
