<?php
/**
 * Plugin Name: NPCWoods LLM-SEO Landing Pages
 * Description: Serves standalone HTML for LLM-optimized city landing pages, bypassing the theme.
 *              Hub-and-spoke URL structure: /uti-treatment/mesa-az/, /uti-treatment/surprise-az/, etc.
 */
add_action( 'template_redirect', function() {
    // Match the full request path so duplicate city slugs under other condition
    // parents do not get intercepted as UTI pages.
    $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $path = trailingslashit($path);

    $path_map = array(
        // UTI Treatment city pages (children of /uti-treatment/)
        '/uti-treatment/mesa-az/'                => 'uti-treatment/mesa-az/index.html',
        '/uti-treatment/surprise-az/'            => 'uti-treatment/surprise-az/index.html',
        '/uti-treatment/scottsdale-az/'          => 'uti-treatment/scottsdale-az/index.html',
        '/uti-treatment/albuquerque-nm/'         => 'uti-treatment/albuquerque-nm/index.html',
        // UTI Treatment intent pages (children of /uti-treatment/)
        '/uti-treatment/burning-when-i-pee/'     => 'uti-treatment/burning-when-i-pee/index.html',
        '/uti-treatment/uti-antibiotics-online/' => 'uti-treatment/uti-antibiotics-online/index.html',
        '/uti-treatment/how-fast-do-uti-antibiotics-work/' => 'uti-treatment/how-fast-do-uti-antibiotics-work/index.html',
        '/uti-treatment/is-my-uti-getting-worse/' => 'uti-treatment/is-my-uti-getting-worse/index.html',
        '/uti-treatment/no-video-uti-treatment/' => 'uti-treatment/no-video-uti-treatment/index.html',
        // Condition hubs (split from former /strep-throat-ear-infection/ on 2026-05-02)
        '/strep-throat-treatment/'              => 'strep-throat-treatment/index.html',
        '/ear-infection-treatment/'             => 'ear-infection-treatment/index.html',
        // Blog posts
        '/blog-burning-when-you-pee-albuquerque/' => 'llmseo/blog-burning-when-you-pee-albuquerque.html',
    );

    if ( is_page() && isset( $path_map[ $path ] ) ) {
        $html_file = ABSPATH . $path_map[ $path ];
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
