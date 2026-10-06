<?php
/**
 * Plugin Name: NPCWoods Site Meta Pixel
 * Description: Pixel install DISABLED 2026-10-06 (HIPAA: no tracking tags). Now only strips Meta Pixel, GTM, GA and Google Ads tags from non-homepage HTML.
 * Version: 3.0
 */

function npcwoods_sitewide_meta_pixel_snippet() {
    // 2026-10-06: Meta Pixel removed sitewide (HIPAA hard rule: no tracking tags). Intentionally empty.
    return '';
}

function npcwoods_sitewide_meta_pixel_rewrite_document($html) {
    if (!is_string($html) || stripos($html, '</head') === false) {
        return $html;
    }

    $patterns = array(
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|/tracking\.js(?:[?"\']))[^"\']*\1[^>]*>\s*</script\s*>~is',
        '~<script\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=).*?</script\s*>~is',
        '~<noscript\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?])).*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
        '~<!--\s*Meta Pixel Code\s*-->~is',
        '~<!--\s*End Meta Pixel Code\s*-->~is',
    );

    $replaced = preg_replace($patterns, '', $html);
    if (is_string($replaced)) {
        $html = $replaced;
    }

    // 2026-10-06: strip only. Never inject a pixel.
    return $html;
}

add_action('template_redirect', function () {
    if (!is_admin() && !is_front_page()) {
        ob_start('npcwoods_sitewide_meta_pixel_rewrite_document');
    }
}, 0);
