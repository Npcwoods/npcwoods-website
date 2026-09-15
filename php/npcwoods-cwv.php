<?php
/**
 * Plugin Name: NPCWoods Core Web Vitals
 * Description: Strip leftover WordPress / Site Designer / WPCode bloat from custom PHP plates so phones can load the homepage.
 * Version: 1.0
 */

if (!defined('ABSPATH')) {
    exit;
}

function npcwoods_cwv_is_custom_plate() {
    if (is_admin()) {
        return false;
    }
    if (is_front_page()) {
        return true;
    }
    if (!is_page()) {
        return false;
    }
    $tpl = (string) get_page_template_slug();
    return strpos($tpl, 'page-npcwoods') !== false;
}

function npcwoods_cwv_dequeue() {
    if (!npcwoods_cwv_is_custom_plate()) {
        return;
    }
    $styles = array(
        'wp-block-library',
        'wp-block-library-theme',
        'global-styles',
        'classic-theme-styles',
        'wp-fonts-local',
        'twentytwentyfour-style',
        'wp-site-designer-contrast-fallback',
        'site-designer-logo-constraints',
    );
    foreach ($styles as $handle) {
        wp_dequeue_style($handle);
        wp_deregister_style($handle);
    }
    $scripts = array(
        'trustedsite-badge-js',
        'googlesitekit-events-provider-content-events',
    );
    foreach ($scripts as $handle) {
        wp_dequeue_script($handle);
        wp_deregister_script($handle);
    }
}
add_action('wp_enqueue_scripts', 'npcwoods_cwv_dequeue', 100);

function npcwoods_cwv_disable_emoji() {
    if (is_admin()) {
        return;
    }
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    add_filter('emoji_svg_url', '__return_false');
}
add_action('init', 'npcwoods_cwv_disable_emoji', 1);

function npcwoods_cwv_strip_custom_css($css) {
    if (npcwoods_cwv_is_custom_plate()) {
        return '';
    }
    return $css;
}
add_filter('wp_get_custom_css', 'npcwoods_cwv_strip_custom_css');

function npcwoods_cwv_disable_wpcode($snippets, $location = '') {
    if (npcwoods_cwv_is_custom_plate()) {
        return array();
    }
    return $snippets;
}
add_filter('wpcode_get_snippets_for_location', 'npcwoods_cwv_disable_wpcode', 10, 2);

function npcwoods_cwv_buffer() {
    if (!npcwoods_cwv_is_custom_plate()) {
        return;
    }
    remove_action('wp_head', 'wp_custom_css_cb', 101);
    if (function_exists('npcwoods_save_contact_button')) {
        remove_action('wp_footer', 'npcwoods_save_contact_button', 90);
    }
    ob_start('npcwoods_cwv_filter_html');
}
add_action('template_redirect', 'npcwoods_cwv_buffer', 0);

function npcwoods_cwv_filter_html($html) {
    if (!is_string($html) || $html === '') {
        return $html;
    }
    $patterns = array(
        '/<style id="wp-site-designer-contrast-fallback">.*?<\/style>/s',
        '/<style id="site-designer-logo-constraints">.*?<\/style>/s',
        '/<style class="wpcode-css-snippet">.*?<\/style>/s',
        '/<style>\s*\/\* ={10,}.*?Professional Redesign.*?<\/style>/s',
        '/<style class="wp-fonts-local">.*?<\/style>/s',
        '/<script[^>]*id="trustedsite-badge-js"[^>]*>.*?<\/script>/s',
        '/<script[^>]*src="https:\/\/cdn\.trustedsite\.com\/js\/1\.js"[^>]*><\/script>/s',
        '/<script id="wp-emoji-settings"[^>]*>.*?<\/script>/s',
        '/<script type="module">\s*\/\*! This file is auto-generated \*\/.*?wp-emoji-loader.*?<\/script>/s',
        '/<script id="googlesitekit-events-provider-content-events-js-before">.*?<\/script>/s',
        '/<script[^>]*id="googlesitekit-events-provider-content-events-js"[^>]*>.*?<\/script>/s',
        '/<link[^>]*href="https:\/\/fonts\.googleapis\.com\/[^"]*"[^>]*>/i',
        '/<link[^>]*href="https:\/\/fonts\.gstatic\.com\/[^"]*"[^>]*>/i',
        '/<link[^>]*rel=["\']preconnect["\'][^>]*href=["\']https:\/\/fonts\.(?:googleapis|gstatic)\.com[^"\']*["\'][^>]*>/i',
        '/<link[^>]*rel=["\']dns-prefetch["\'][^>]*href=["\']https:\/\/fonts\.(?:googleapis|gstatic)\.com[^"\']*["\'][^>]*>/i',
        '/<script[^>]*src=["\']https:\/\/img1\.wsimg\.com\/[^"\']+["\'][^>]*>.*?<\/script>/s',
        '/var trafficScript = document\.createElement\(\'script\'\); trafficScript\.src = \'https:\/\/img1\.wsimg\.com[^;]+; window\.document\.head\.appendChild\(trafficScript\);/',
    );
    foreach ($patterns as $pattern) {
        $html = preg_replace($pattern, '', $html);
    }
    return $html;
}
