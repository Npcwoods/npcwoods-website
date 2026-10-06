<?php
/**
 * Plugin Name: NPCWoods Static Pages
 * Description: Serves standalone HTML for state landing pages, conditions hub, and sitemap
 */
add_action( "template_redirect", function() {
    $page_map = array(
        "faq" => "faq/index.html",
        "arizona-telemedicine" => "arizona-telemedicine/index.html",
        "arizona-uti-treatment" => "arizona-uti-treatment/index.html",
        "conditions"             => "conditions/index.html",
        "sitemap"                => "sitemap/index.html",
        "uti-treatment"          => "uti-treatment/index.html",
        "sinus-infection-treatment" => "sinus-infection-treatment/index.html",
        "cold-sore-treatment"    => "cold-sore-treatment/index.html",
        "colorado-telemedicine"  => "colorado-telemedicine/index.html",
        "georgia-telemedicine"   => "georgia-telemedicine/index.html",
        "idaho-telemedicine"     => "idaho-telemedicine/index.html",
        "iowa-telemedicine"      => "iowa-telemedicine/index.html",
        "montana-telemedicine"   => "montana-telemedicine/index.html",
        "nevada-telemedicine"    => "nevada-telemedicine/index.html",
        "new-mexico-telemedicine"=> "new-mexico-telemedicine/index.html",
        "north-carolina-telemedicine" => "north-carolina-telemedicine/index.html",
        "oregon-telemedicine"    => "oregon-telemedicine/index.html",
        "utah-telemedicine"      => "utah-telemedicine/index.html",
        "washington-telemedicine" => "washington-telemedicine/index.html",
        "trust-video"            => "trust-video/index.html",
        "ed-treatment"           => "ed-treatment/index.html",        "pricing"                    => "pricing/index.html",        "credentials"                => "credentials/index.html",
        "do-i-need-antibiotics-sinus-infection" => "do-i-need-antibiotics-sinus-infection/index.html",

        "real-care"              => "real-care/index.html",
        "notice-of-privacy-practices" => "notice-of-privacy-practices/index.html",
        "what-is-async-telemedicine" => "what-is-async-telemedicine/index.html",
        "athens-saturday-text-visit" => "athens-saturday-text-visit/index.html",
        "florida-vacation-sick-text-visit" => "florida-vacation-sick-text-visit/index.html",
        "florida-beach-sick-text-visit" => "florida-beach-sick-text-visit/index.html",
        "seattle-gameday-text-visit" => "seattle-gameday-text-visit/index.html",
        "seattle-needle-text-visit" => "seattle-needle-text-visit/index.html",
        "panama-city-beach-text-visit" => "panama-city-beach-text-visit/index.html",
        "vegas-strip-text-visit" => "vegas-strip-text-visit/index.html",
        "salt-lake-ski-text-visit" => "salt-lake-ski-text-visit/index.html",
        "provo-y-text-visit" => "provo-y-text-visit/index.html",
        "bozeman-text-visit" => "bozeman-text-visit/index.html",
        "red-rocks-text-visit" => "red-rocks-text-visit/index.html",
        "denver-sunday-text-visit" => "denver-sunday-text-visit/index.html",

        "san-juan-county-text-visit" => "san-juan-county-text-visit/index.html",
        "torrance-county-text-visit" => "torrance-county-text-visit/index.html",
        "pershing-county-text-visit" => "pershing-county-text-visit/index.html",
        "baker-county-text-visit" => "baker-county-text-visit/index.html",
        "colfax-county-text-visit" => "colfax-county-text-visit/index.html",
        "humboldt-county-text-visit" => "humboldt-county-text-visit/index.html",
        "emery-county-text-visit" => "emery-county-text-visit/index.html",
        "park-county-text-visit" => "park-county-text-visit/index.html",
        "winnebago-county-text-visit" => "winnebago-county-text-visit/index.html",
    );

    $slug = get_post_field( "post_name", get_queried_object_id() );

    if ( ( is_page() || is_single() ) && isset( $page_map[ $slug ] ) ) {
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
