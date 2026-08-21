<?php
/**
 * Plugin Name: NPCWoods Retired Meta Pixel Guard
 * Description: Removes retired Meta and legacy third-party tracking from public HTML responses.
 * Version: 1.1
 */

function npcwoods_sitewide_meta_pixel_rewrite_document($html) {
    if (!is_string($html) || stripos($html, '</head') === false) {
        return $html;
    }

    $patterns = array(
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|/tracking\.js(?:[?"\']))[^"\']*\1[^>]*>\s*</script\s*>~is',
        '~<script\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=).*?</script\s*>~is',
        '~<noscript\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?])).*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
    );

    $html = preg_replace($patterns, '', $html);

    return $html;
}

add_action('template_redirect', function () {
    // The homepage owns its exact Pixel directly in its template. Avoiding a
    // response-level rewrite here preserves the complete homepage document.
    if (!is_admin() && !is_front_page()) {
        ob_start('npcwoods_sitewide_meta_pixel_rewrite_document');
    }
}, 0);
