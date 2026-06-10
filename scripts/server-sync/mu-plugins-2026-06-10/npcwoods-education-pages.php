<?php
/**
 * Plugin Name: NPCWoods Patient Education Pages
 * Description: Serves static HTML files for /learn/ and /medications/ patient education library.
 *              Bypasses WordPress block theme to serve raw HTML with all scripts/styles intact.
 * Version: 1.1
 * Author: NPCWoods
 */

add_action( 'template_redirect', function() {
    // Map page slugs to their static HTML files
    $page_map = array(
        // Hub page
        'learn'                   => 'learn/index.html',
        // Condition education pages
        'strep-throat'            => 'learn/strep-throat/index.html',
        'uti'                     => 'learn/uti/index.html',
        'sinus-infection'         => 'learn/sinus-infection/index.html',
        'tooth-infection'         => 'learn/tooth-infection/index.html',
        'ear-infection'           => 'learn/ear-infection/index.html',
        'stomach-bug'             => 'learn/stomach-bug/index.html',
        'pink-eye'                => 'learn/pink-eye/index.html',
        'bronchitis'              => 'learn/bronchitis/index.html',
        'skin-infection'          => 'learn/skin-infection/index.html',
        'allergic-reaction'       => 'learn/allergic-reaction/index.html',
        'cold-sores'              => 'learn/cold-sores/index.html',
        'yeast-infection'         => 'learn/yeast-infection/index.html',
        'ingrown-toenail'         => 'learn/ingrown-toenail/index.html',
        'covid-flu'               => 'learn/covid-flu/index.html',
        // Drug reference pages
        'amoxicillin'             => 'medications/amoxicillin/index.html',
        'augmentin'               => 'medications/augmentin/index.html',
        'azithromycin'            => 'medications/azithromycin/index.html',
        'penicillin'              => 'medications/penicillin/index.html',
        'doxycycline'             => 'medications/doxycycline/index.html',
        'cephalexin'              => 'medications/cephalexin/index.html',
        'clindamycin'             => 'medications/clindamycin/index.html',
        'metronidazole'           => 'medications/metronidazole/index.html',
        'nitrofurantoin'          => 'medications/nitrofurantoin/index.html',
        'tmp-smx'                 => 'medications/tmp-smx/index.html',
        'fluconazole'             => 'medications/fluconazole/index.html',
        'valacyclovir'            => 'medications/valacyclovir/index.html',
        'ondansetron'             => 'medications/ondansetron/index.html',
        'hydroxyzine'             => 'medications/hydroxyzine/index.html',
        'prednisone'              => 'medications/prednisone/index.html',
        'mupirocin'               => 'medications/mupirocin/index.html',
        'benzonatate'             => 'medications/benzonatate/index.html',
        'oseltamivir'             => 'medications/oseltamivir/index.html',
        'paxlovid'                => 'medications/paxlovid/index.html',
        'erythromycin-ophthalmic' => 'medications/erythromycin-ophthalmic/index.html',
        'polytrim'                => 'medications/polytrim/index.html',
        // Medications parent page (no standalone HTML, but keep for future)
        'medications'             => 'medications/index.html',
    );

    $slug = get_post_field( 'post_name', get_queried_object_id() );

    if ( is_page() && isset( $page_map[ $slug ] ) ) {
        $html_file = ABSPATH . $page_map[ $slug ];
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            header( 'X-NPCWoods-Page: education' );
            header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
            header( 'X-Content-Type-Options: nosniff' );
            header( 'X-Frame-Options: SAMEORIGIN' );
            header( 'Referrer-Policy: strict-origin-when-cross-origin' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
