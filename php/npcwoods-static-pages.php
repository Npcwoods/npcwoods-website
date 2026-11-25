<?php
/**
 * Plugin Name: NPCWoods Static Pages
 * Description: Serves standalone HTML for state landing pages, conditions hub, and sitemap
 */
add_action( "template_redirect", function() {
    // Nested series pages need path matching (their stop slugs repeat across series,
    // and /learn/screening-labs/ shares a slug with the /screening-labs/ offer page).
    $path_map = array(
        "/learn/screening-labs/" => "learn/screening-labs/index.html",
        "/learn/screening-labs/metabolic-panel/" => "learn/screening-labs/metabolic-panel/index.html",
        "/learn/screening-labs/cholesterol/" => "learn/screening-labs/cholesterol/index.html",
        "/learn/screening-labs/a1c/" => "learn/screening-labs/a1c/index.html",
        "/learn/screening-labs/thyroid/" => "learn/screening-labs/thyroid/index.html",
        "/learn/screening-labs/cbc/" => "learn/screening-labs/cbc/index.html",
        "/learn/screening-labs/who-and-how-often/" => "learn/screening-labs/who-and-how-often/index.html",
        "/learn/screening-labs/reading-results/" => "learn/screening-labs/reading-results/index.html",
        "/learn/mastitis/" => "learn/mastitis/index.html",
        "/learn/mastitis/how-it-starts/" => "learn/mastitis/how-it-starts/index.html",
        "/learn/mastitis/what-it-feels-like/" => "learn/mastitis/what-it-feels-like/index.html",
        "/learn/mastitis/lookalikes/" => "learn/mastitis/lookalikes/index.html",
        "/learn/mastitis/comfort-at-home/" => "learn/mastitis/comfort-at-home/index.html",
        "/learn/mastitis/red-flags/" => "learn/mastitis/red-flags/index.html",
        "/learn/mastitis/keep-feeding/" => "learn/mastitis/keep-feeding/index.html",
        "/learn/mastitis/text-vs-in-person/" => "learn/mastitis/text-vs-in-person/index.html",
    );
    $req_path = trailingslashit( (string) parse_url( $_SERVER["REQUEST_URI"], PHP_URL_PATH ) );
    if ( isset( $path_map[ $req_path ] ) ) {
        $html_file = ABSPATH . $path_map[ $req_path ];
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

    $page_map = array(
        "faq" => "faq/index.html",
        "cheap-urgent-care-no-insurance" => "cheap-urgent-care-no-insurance/index.html",
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
        "out-of-town-medication-refill" => "out-of-town-medication-refill/index.html",
        "sick-on-vacation-text-visit" => "sick-on-vacation-text-visit/index.html",
        "travel-telehealth-text-visit" => "travel-telehealth-text-visit/index.html",
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
    "lincoln-county-text-visit" => "lincoln-county-text-visit/index.html",
    "rosebud-county-text-visit" => "rosebud-county-text-visit/index.html",
    "costilla-county-text-visit" => "costilla-county-text-visit/index.html",
    "storey-county-text-visit" => "storey-county-text-visit/index.html",
    "mckinley-county-text-visit" => "mckinley-county-text-visit/index.html",
    "baca-county-text-visit" => "baca-county-text-visit/index.html",
    "wayne-county-text-visit" => "wayne-county-text-visit/index.html",
    "closest-urgent-care" => "closest-urgent-care/index.html",
    "teton-county-text-visit" => "teton-county-text-visit/index.html",
    "lander-county-text-visit" => "lander-county-text-visit/index.html",
    "taylor-county-text-visit" => "taylor-county-text-visit/index.html",
    "guadalupe-county-text-visit" => "guadalupe-county-text-visit/index.html",
    "conejos-county-text-visit" => "conejos-county-text-visit/index.html",
    "mineral-county-text-visit" => "mineral-county-text-visit/index.html",
    "rich-county-text-visit" => "rich-county-text-visit/index.html",
    "island-county-text-visit" => "island-county-text-visit/index.html",
    "rio-arriba-county-text-visit" => "rio-arriba-county-text-visit/index.html",
    "dolores-county-text-visit" => "dolores-county-text-visit/index.html",
    "liberty-county-text-visit" => "liberty-county-text-visit/index.html",
    "greene-county-text-visit" => "greene-county-text-visit/index.html",
    "boise-county-text-visit" => "boise-county-text-visit/index.html",
    "eureka-county-text-visit" => "eureka-county-text-visit/index.html",
    "washington-uti-treatment" => "washington-uti-treatment/index.html",
    "screening-labs" => "screening-labs/index.html",
    "mastitis-treatment" => "mastitis-treatment/index.html",
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
