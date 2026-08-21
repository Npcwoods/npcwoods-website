<?php
/**
 * Plugin Name: NPCWoods Tracking
 * Description: Removes retired third-party tracking from public HTML responses.
 * Version: 2.1
 */

/**
 * Covers WordPress templates plus every static HTML page served by the site's
 * mu-plugins. Removing the legacy snippets from the final response also
 * catches tags injected by Site Kit or other WordPress plugins.
 */
function npcwoods_tracking_rewrite_document($html) {
    if (!is_string($html) || stripos($html, '</head') === false) {
        return $html;
    }

    $patterns = array(
        // External Google scripts and the legacy first-party event layer.
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|/tracking\.js(?:[?"\']))[^"\']*\1[^>]*>\s*</script\s*>~is',
        // Inline GTM/gtag bootstraps, the previous Meta Pixel, and Meta no-op stubs.
        '~<script\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=).*?</script\s*>~is',
        // GTM and legacy Pixel no-script fallbacks.
        '~<noscript\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?])).*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
    );

    $html = preg_replace($patterns, '', $html);

    return $html;
}

/**
 * The homepage embeds the approved Pixel in its own template immediately
 * after wp_head(). Strip any legacy or duplicate tracker emitted by a
 * WordPress head hook without buffering the homepage body.
 */
function npcwoods_tracking_rewrite_homepage_head($html) {
    if (!is_string($html)) {
        return $html;
    }

    $patterns = array(
        '~<!--\s*Meta Pixel Code\s*-->.*?<!--\s*End Meta Pixel Code\s*-->~is',
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net)[^"\']*\1[^>]*>\s*</script\s*>~is',
        '~<script\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=).*?</script\s*>~is',
        '~<noscript\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?])).*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
    );

    return preg_replace($patterns, '', $html);
}

function npcwoods_tracking_start_homepage_head_buffer() {
    if (!is_admin() && is_front_page()) {
        $GLOBALS['npcwoods_tracking_homepage_head_buffer_started'] = ob_start('npcwoods_tracking_rewrite_homepage_head');
    }
}

function npcwoods_tracking_end_homepage_head_buffer() {
    if (!empty($GLOBALS['npcwoods_tracking_homepage_head_buffer_started'])) {
        ob_end_flush();
        unset($GLOBALS['npcwoods_tracking_homepage_head_buffer_started']);
    }
}

add_action('wp_head', 'npcwoods_tracking_start_homepage_head_buffer', 0);
add_action('wp_head', 'npcwoods_tracking_end_homepage_head_buffer', PHP_INT_MAX);

// Start before the static-page handlers (which use readfile() at priority 1).
add_action('template_redirect', function () {
    // The homepage owns its exact Pixel directly in its template. Avoiding a
    // response-level rewrite here preserves the complete homepage document.
    if (!is_admin() && !is_front_page()) {
        ob_start('npcwoods_tracking_rewrite_document');
    }
}, 0);
