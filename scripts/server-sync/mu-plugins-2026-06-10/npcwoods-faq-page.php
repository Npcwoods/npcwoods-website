<?php
/**
 * Plugin Name: NPCWoods FAQ Page
 * Description: Serves static HTML for /faq/ page
 */
add_action('template_redirect', function() {
    if (is_page('faq')) {
        $file = ABSPATH . 'faq/index.html';
        if (file_exists($file)) {
            readfile($file);
            exit;
        }
    }
});
