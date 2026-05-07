<?php
/**
 * Plugin Name: NPCWoods LLM-SEO Landing Pages
 * Description: Serves standalone HTML for LLM-optimized city landing pages, bypassing the theme.
 *              Hub-and-spoke URL structure: /uti-treatment/mesa-az/, /uti-treatment/surprise-az/, etc.
 */
add_action( 'template_redirect', function() {
    // City pages nested under condition hubs (hub-and-spoke SEO structure)
    $page_map = array(
        // UTI Treatment city pages (children of /uti-treatment/)
        'mesa-az'                               => 'uti-treatment/mesa-az/index.html',
        'surprise-az'                           => 'uti-treatment/surprise-az/index.html',
        'scottsdale-az'                         => 'uti-treatment/scottsdale-az/index.html',
        'albuquerque-nm'                        => 'uti-treatment/albuquerque-nm/index.html',
        // Condition hubs (split from former /strep-throat-ear-infection/ on 2026-05-02)
        'strep-throat-treatment'                => 'strep-throat-treatment/index.html',
        'ear-infection-treatment'               => 'ear-infection-treatment/index.html',
        // Blog posts
        'blog-burning-when-you-pee-albuquerque' => 'llmseo/blog-burning-when-you-pee-albuquerque.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
            header( 'X-Content-Type-Options: nosniff' );
            header( 'X-Frame-Options: SAMEORIGIN' );
            header( 'Referrer-Policy: strict-origin-when-cross-origin' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
