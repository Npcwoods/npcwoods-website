<?php
/**
 * Plugin Name: NPCWoods Corneal Abrasion Blog Route
 * Description: Serves the standalone, search-safe corneal abrasion education article.
 */

function npcwoods_corneal_remove_meta_pixel($html) {
    return preg_replace('/<!--\s*Meta Pixel Code\s*-->.*?<!--\s*End Meta Pixel Code\s*-->\s*/is', '', $html);
}

add_action('template_redirect', function () {
    if (!is_singular('post')) return;

    $post = get_post();
    if (!$post || $post->post_name !== 'scratched-eye-corneal-abrasion-care') return;

    $html_file = ABSPATH . 'corneal-abrasion-eye-scratch/index.html';
    if (!file_exists($html_file)) return;

    header('Content-Type: text/html; charset=UTF-8');
    header('X-NPCWoods-Page: corneal-abrasion-blog');
    header('Strict-Transport-Security: max-age=31536000; includeSubDomains; preload');
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    ob_start('npcwoods_corneal_remove_meta_pixel');
    readfile($html_file);
    exit;
}, 1);
