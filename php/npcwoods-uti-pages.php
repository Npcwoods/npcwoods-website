<?php
/**
 * Plugin Name: NPCWoods UTI Explained Pages
 * Description: Serves standalone HTML for /learn/uti/ explainer series stops (hub remains on education plugin if present; path_map wins for nested stops).
 */

add_action( 'template_redirect', function() {
    $path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
    $path = trailingslashit( $path );

    $path_map = array(
        '/learn/uti/'                      => 'learn/uti/index.html',
        '/learn/uti/how-it-starts/'        => 'learn/uti/how-it-starts/index.html',
        '/learn/uti/what-it-feels-like/'    => 'learn/uti/what-it-feels-like/index.html',
        '/learn/uti/lookalikes/'           => 'learn/uti/lookalikes/index.html',
        '/learn/uti/bladder-vs-kidney/'    => 'learn/uti/bladder-vs-kidney/index.html',
        '/learn/uti/antibiotics/'          => 'learn/uti/antibiotics/index.html',
        '/learn/uti/relief/'               => 'learn/uti/relief/index.html',
        '/learn/uti/recurring/'            => 'learn/uti/recurring/index.html',
        '/learn/uti/prevention/'           => 'learn/uti/prevention/index.html',
        '/learn/uti/who-needs-in-person/'  => 'learn/uti/who-needs-in-person/index.html',
        '/learn/uti/myths/'                => 'learn/uti/myths/index.html',
    );

    $html_rel = null;
    if ( isset( $path_map[ $path ] ) ) {
        $html_rel = $path_map[ $path ];
    } else {
        $slug_map = array(
            'uti'                 => 'learn/uti/index.html',
            'how-it-starts'       => 'learn/uti/how-it-starts/index.html',
            'what-it-feels-like'  => 'learn/uti/what-it-feels-like/index.html',
            'lookalikes'          => 'learn/uti/lookalikes/index.html',
            'bladder-vs-kidney'   => 'learn/uti/bladder-vs-kidney/index.html',
            'antibiotics'         => 'learn/uti/antibiotics/index.html',
            'relief'              => 'learn/uti/relief/index.html',
            'recurring'           => 'learn/uti/recurring/index.html',
            'prevention'          => 'learn/uti/prevention/index.html',
            'who-needs-in-person' => 'learn/uti/who-needs-in-person/index.html',
            'myths'               => 'learn/uti/myths/index.html',
        );
        $slug = get_post_field( 'post_name', get_queried_object_id() );
        if ( is_page() && isset( $slug_map[ $slug ] ) ) {
            // Only claim nested explainer slugs via slug_map when parent path is UTI,
            // OR when the path already matched. For bare slug collisions, require path prefix.
            if ( strpos( $path, '/learn/uti/' ) === 0 || $slug === 'uti' ) {
                $html_rel = $slug_map[ $slug ];
            }
        }
    }

    if ( $html_rel ) {
        $html_file = ABSPATH . $html_rel;
        if ( file_exists( $html_file ) ) {
            header( 'Content-Type: text/html; charset=UTF-8' );
            header( 'X-NPCWoods-Page: uti-explained' );
            header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
            header( 'X-Content-Type-Options: nosniff' );
            header( 'X-Frame-Options: SAMEORIGIN' );
            header( 'Referrer-Policy: strict-origin-when-cross-origin' );
            readfile( $html_file );
            exit;
        }
    }
}, 1 );
