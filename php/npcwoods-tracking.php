<?php
/**
 * Plugin Name: NPCWoods Tracking
 * Description: Installs the canonical Meta Pixel on every HTML page and removes legacy Google and Meta tracking.
 * Version: 2.0
 */

/**
 * Keep this string byte-for-byte aligned with the Meta Pixel code supplied by Chris.
 */
function npcwoods_meta_pixel_snippet() {
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

    return preg_replace(
        '~</head\s*>~i',
        npcwoods_meta_pixel_snippet() . "\n</head>",
        $html,
        1
    );
}

// Start before the static-page handlers (which use readfile() at priority 1).
add_action('template_redirect', function () {
    if (!is_admin()) {
        ob_start('npcwoods_tracking_rewrite_document');
    }
}, 0);

// Ahrefs is intentionally retained; Chris asked only to remove Meta/Google tracking.
add_action('wp_head', function () {
    echo '<!-- NPCWoods Tracking: Ahrefs Analytics -->' . "\n";
    echo '<script src="https://analytics.ahrefs.com/analytics.js" data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>' . "\n";
}, 1);
