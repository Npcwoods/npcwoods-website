<?php
/**
 * Plugin Name: NPCWoods Tracking (GA4 fallback + tracking.js)
 * Description: Adds the canonical GA4 tag and tracking.js event layer. GTM is already installed via Site Kit or similar.
 * Version: 1.1
 *
 * GTM-59QSWZRC is already injected by another plugin — do NOT duplicate it.
 * The site should emit neutral click events only; downstream conversion
 * handling belongs in GTM / GA4 / Google Ads, not inline page code.
 */

function npcwoods_is_health_condition_request() {
    $uri = isset($_SERVER['REQUEST_URI']) ? strtolower((string) $_SERVER['REQUEST_URI']) : '';
    // Same family as tests/guardian/build_manifest.py HEALTH_MARKERS.
    $markers = array(
        'uti',
        'sinus',
        'strep',
        'ear-infection',
        'tooth',
        'dental',
        '/learn/',
        '/medications/',
        'ed-treatment',
        'glp1',
        'yeast',
        'antibiotics',
        '/conditions/',
        'poison-ivy',
        'cold-sore',
    );
    foreach ($markers as $marker) {
        // Avoid a false match on /executive/ (contains the letters "uti").
        if ($marker === 'uti' && strpos($uri, 'executive') !== false) {
            continue;
        }
        if (strpos($uri, $marker) !== false) {
            return true;
        }
    }
    return false;
}

// GA4 + Google Ads base tags — homepage / marketing only. Health-condition
// URLs stay off GTM/GA4/Ads (no BAA).
add_action('wp_head', function () {
    if (npcwoods_is_health_condition_request()) {
        echo "<!-- Meta, GTM, GA4, and Google Ads stay off health-condition pages (no BAA). -->\n";
        return;
    }
    ?>
    <!-- NPCWoods Tracking: GA4 + Ads direct -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EFFRQMG8TC"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-EFFRQMG8TC');
    gtag('config', 'AW-610222919');
    </script>
    <!-- NPCWoods Tracking: Ahrefs Analytics -->
    <script src="https://analytics.ahrefs.com/analytics.js" data-key="1qFceGSHKP6yg4JlSdNJ4Q" async></script>
    <?php
}, 1);

// Canonical site event layer before </body>
add_action('wp_footer', function () {
    ?>
    <!-- NPCWoods Tracking: tracking.js -->
    <script src="/tracking.js?v=20260528-no-phi"></script>
    <?php
}, 99);
