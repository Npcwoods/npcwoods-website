<?php
/**
 * Plugin Name: NPCWoods Tracking (DEFANGED — injects nothing)
 * Description: Strip-only. Removes GTM / GA / Google Ads / Meta Pixel tags from public HTML (and duplicate pixels from the homepage wp_head). Injects NO tracking code.
 * Version: 4.1
 */

/*
 * ###########################################################################
 * ##                                                                       ##
 * ##   DO NOT RE-ADD A META PIXEL (OR ANY TRACKER) INJECTION TO THIS FILE  ##
 * ##                                                                       ##
 * ###########################################################################
 *
 * WHY THIS PLUGIN INJECTS NOTHING (HIPAA)
 * ---------------------------------------
 * NPCWoods has NO Business Associate Agreement (BAA) with Meta (Facebook),
 * Ahrefs, or Google's advertising/analytics products. Most public pages on
 * npcwoods.com are health-condition, medication, or treatment pages (UTI,
 * sinus, strep, ED, GLP-1, medications, /learn/, blogs...). A Meta Pixel
 * PageView on those URLs tells Meta that an identifiable browser looked up a
 * specific health condition. That is a HIPAA problem (see HHS OCR guidance on
 * online tracking technologies). Live pages were cleaned on 2026-10-08.
 *
 * Earlier versions of this file (v3.0) stripped the health-page no-op fbq stub
 * and then injected the full Meta Pixel 1428464038973925 (fbevents.js +
 * fbq('init') + fbq('track','PageView') + facebook.com/tr noscript image)
 * before </head> on EVERY page except the homepage. That silently undid the
 * health-page cleanup. This version:
 *   - keeps the tag-STRIPPING behavior (GTM, GA4, Google Ads, DoubleClick,
 *     /tracking.js, Meta fbevents.js / fbq() calls / facebook.com/tr pixels);
 *   - NO LONGER strips the `window.fbq = function () {};` no-op stub, because
 *     that stub is what blocks a later-injected Meta pixel on health pages;
 *   - injects NOTHING. There is no snippet function and no </head> rewrite.
 *   - keeps the homepage wp_head de-duplication buffer (strip only); the
 *     homepage's own tracking lives in homepage/page-npcwoods-home.php.
 *
 * Any future marketing tracking must be scoped to explicitly non-health pages
 * and reviewed for HIPAA first. tests/test_sitewide_meta_tracking.py fails if
 * this file injects a tracker.
 */

/**
 * Covers WordPress templates plus every static HTML page served by the site's
 * mu-plugins. Strips GTM/GA/Ads and Meta Pixel tags. Injects nothing.
 */
function npcwoods_tracking_rewrite_document($html) {
    if (!is_string($html) || stripos($html, '</head') === false) {
        return $html;
    }

    $patterns = array(
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|connect\.facebook\.net|/tracking\.js(?:[?"\']))[^"\']*\1[^>]*>\s*</script\s*>~is',
        '~<script\b[^>]*>(?:(?!</script).)*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\()(?:(?!</script).)*?</script\s*>~is',
        '~<noscript\b[^>]*>(?:(?!</noscript).)*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?]))(?:(?!</noscript).)*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
        '~<!--\s*Meta Pixel Code\s*-->~is',
        '~<!--\s*End Meta Pixel Code\s*-->~is',
    );

    $replaced = preg_replace($patterns, '', $html);
    return is_string($replaced) ? $replaced : $html;
}

/**
 * The homepage embeds both Pixels in its own template immediately after
 * wp_head(). Strip plugin duplicates from wp_head without buffering the body.
 */
function npcwoods_tracking_rewrite_homepage_head($html) {
    if (!is_string($html)) {
        return $html;
    }

    $patterns = array(
        '~<!--\s*Meta Pixel Code\s*-->.*?<!--\s*End Meta Pixel Code\s*-->~is',
        '~<script\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net)[^"\']*\1[^>]*>\s*</script\s*>~is',
        '~<script\b[^>]*>(?:(?!</script).)*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=)(?:(?!</script).)*?</script\s*>~is',
        '~<noscript\b[^>]*>(?:(?!</noscript).)*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?]))(?:(?!</noscript).)*?</noscript\s*>~is',
        '~<img\b[^>]*\bsrc\s*=\s*(["\'])[^"\']*facebook\.com/tr(?:[/?])[^"\']*\1[^>]*>~is',
    );

    $replaced = preg_replace($patterns, '', $html);
    return is_string($replaced) ? $replaced : $html;
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

add_action('template_redirect', function () {
    if (!is_admin() && !is_front_page()) {
        ob_start('npcwoods_tracking_rewrite_document');
    }
}, 0);
