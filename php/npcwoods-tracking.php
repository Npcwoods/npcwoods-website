<?php
/**
 * Plugin Name: NPCWoods Tracking
 * Description: Keeps site pixel 1428464038973925 on public pages; strips GTM/GA/ads pixel 1558261907814968 off non-homepage HTML.
 * Version: 3.0
 */

function npcwoods_site_pixel_snippet() {
    return <<<'HTML'
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1428464038973925');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1428464038973925&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
HTML;
}

/**
 * Covers WordPress templates plus every static HTML page served by the site's
 * mu-plugins. Strips GTM/GA/ads pixel, then installs the site Meta Pixel.
 */
function npcwoods_tracking_rewrite_document($html) {
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

    return preg_replace('~</head\s*>~i', npcwoods_site_pixel_snippet() . '</head>', $html, 1);
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
        '~<script\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|\bgtag\s*\(|\bdataLayer\s*=|connect\.facebook\.net/en_US/fbevents\.js|\bfbq\s*\(|window\.fbq\s*=).*?</script\s*>~is',
        '~<noscript\b[^>]*>.*?(?:googletagmanager\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net|facebook\.com/tr(?:[/?])).*?</noscript\s*>~is',
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
