<?php
/**
 * Plugin Name: NPCWoods 301 Redirects
 * Description: Redirects old/removed pages + disables author archives
 */
add_action("init", function() {
    $redirects = [
        "/activity.json/"            => "/wp-content/uploads/npc-data/activity.json",
        "/status.json/"              => "/wp-content/uploads/npc-data/status.json",
        "/scottsdale-uti-treatment/"   => "/uti-treatment/scottsdale-az/",
        "/mesa-uti-treatment/"         => "/uti-treatment/mesa-az/",
        "/mesa-az-uti/"               => "/uti-treatment/mesa-az/",
        "/surprise-uti-treatment/"     => "/uti-treatment/surprise-az/",
        "/albuquerque-uti-treatment/"  => "/uti-treatment/albuquerque-nm/",
        "/atlanta-uti-treatment/"     => "/uti-treatment/",
        "/boone-sinus-infection/"     => "/sinus-infection-treatment/",
        "/phoenix-az-sinus/"          => "/sinus-infection-treatment/phoenix-az/",
        "/sample-page/"              => "/",
        "/hello-world/"              => "/",
        "/my-account/"               => "/",
        "/checkout/"                 => "/",
        "/cart/"                     => "/",
        "/shop/"                     => "/",
        "/author/admin/"             => "/about/",
        "/author/chris/"             => "/about/",
        "/author/npcwoods/"          => "/about/",
        "/gilbert-az-strep/"         => "/arizona-telemedicine/",
        "/tucson-az-uti/"            => "/uti-treatment/tucson-az/",
        "/blog/blog-ry/"             => "/blog/",
        "/blog/blog-ry"              => "/blog/",
        "/blog/burning-when-you-pee-albuquerque/" => "/learn/uti/what-it-feels-like/",
        "/experience/"               => "/patient-experience/",
        "/ear-infection/"            => "/ear-infection-treatment/",
        "/cost-savings-preview/"     => "/pricing/",
        "/swimmers-ear-preview/"     => "/ear-pain-after-swimming-swimmers-ear/",
        "/affordable-telemedicine-arizona-no-insurance/" => "/pricing/",
        "/conditions/albuterol-inhaler-refill-preview/" => "/conditions/",
        "/pharmacy-info/"            => "/pharmacy/",
        "/states/"                   => "/",
        "/phoenix-telemedicine/"      => "/arizona-telemedicine/",
        "/home/phoenix-telemedicine/" => "/arizona-telemedicine/",
        "/tucson-telemedicine/"       => "/arizona-telemedicine/",
        "/uti/"                       => "/uti-treatment/",
        "/sinus/"                     => "/sinus-infection-treatment/",
        "/strep/"                     => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/" => "/strep-throat-treatment/",
        // Phoenix/Tucson sinus short paths were 301ing to UTI city pages (~Sep 24).
        // Send guests to the matching sinus city plates (2026-10-06).
        "/sinus-treatment/phoenix-az/" => "/sinus-infection-treatment/phoenix-az/",
        "/sinus/phoenix-az/" => "/sinus-infection-treatment/phoenix-az/",
        "/sinus-treatment/tucson-az/" => "/sinus-infection-treatment/tucson-az/",
        "/sinus/tucson-az/" => "/sinus-infection-treatment/tucson-az/",
        // Atlanta/Charlotte leftover city tents were serving UTI food (2026-08-29).
        // Send guests to the matching condition plate, not the UTI table.
        "/ed-treatment/atlanta-ga/" => "/ed-treatment/",
        "/ed-treatment/charlotte-nc/" => "/ed-treatment/",
        "/sinus-infection-treatment/atlanta-ga/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/charlotte-nc/" => "/sinus-infection-treatment/",
        "/strep-throat-ear-infection/atlanta-ga/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/charlotte-nc/" => "/strep-throat-treatment/",
        // Guardrail slug cleanup (2026-04-12) — removed "doctor"/"insurance" from URLs
        "/do-i-need-doctor-for-uti/"              => "/when-to-see-provider-for-uti/",
        "/uti-antibiotics-without-seeing-a-doctor/" => "/uti-treatment/",
        "/urgent-care-cost-without-insurance/"    => "/urgent-care-price-guide/",
        // 503 crawl waste (2026-10-06) — send guests to healthy siblings
        "/can-a-nurse-practitioner-prescribe-in-north-carolina/" => "/north-carolina-telemedicine/",
        "/uti-treatment/uti-or-yeast-infection/" => "/learn/uti/lookalikes/",
        // 404 stub tidy (2026-10-07) — Chris approved 301s
        "/north-carolina-prescribe/" => "/north-carolina-telemedicine/",
        "/yeast-infection-lookalikes/" => "/learn/uti/lookalikes/",
        // Duplicate plates retired (2026-10-15) — Chris: "Please fix the duplicate pages"
        "/landing-pages/uti-treatment/" => "/uti-treatment/",
        "/landing-pages/medications/amoxicillin/" => "/medications/amoxicillin/",
        // Blog fold (2026-10-17) — Chris approved the blog plan: "push it live".
        // Thin/duplicate posts fold into the stronger page. One hop, no chains.
        "/out-of-pocket-59-flat-fee-nurse-practitioner/" => "/pricing/",
        "/cash-pay-telehealth-reasons/" => "/pricing/",
        "/cost-savings-convenience/" => "/pricing/",
        "/is-text-based-telehealth-safe/" => "/what-is-async-telemedicine/",
        "/text-based-vs-video-telehealth/" => "/what-is-async-telemedicine/",
        "/telehealth-vs-urgent-care-cost-speed/" => "/telehealth-vs-urgent-care/",
        "/tooth-infection-antibiotics-telehealth/" => "/dental-pain/",
        "/get-uti-antibiotics-online-same-day/" => "/uti-treatment/uti-antibiotics-online/",
        "/burning-when-i-pee/" => "/learn/uti/what-it-feels-like/",
        "/uti-treatment/burning-when-i-pee/" => "/learn/uti/what-it-feels-like/",
        "/blog-burning-when-you-pee-albuquerque/" => "/learn/uti/what-it-feels-like/",
        "/is-it-allergies-or-a-sinus-infection/" => "/allergies-vs-sinus-infection/",
        "/stop-popping-benadryl/" => "/allergies-vs-sinus-infection/",
        "/common-infections-telehealth-same-day/" => "/what-can-telehealth-prescribe/",
        "/questions-before-online-health-service/" => "/alternatives-to-teladoc/",
        "/red-eye-after-swimming-pink-eye-or-pool-irritation/" => "/pink-eye-treatment/",
        "/heat-rash-or-skin-infection/" => "/learn/skin-infection/",
        "/wet-bathing-suit-yeast-infection-or-irritation/" => "/yeast-infection-treatment-online/",
        "/can-allergies-cause-a-cough-or-is-it-bronchitis/" => "/learn/bronchitis/",
        "/blog/can-nurse-practitioner-prescribe-antibiotics-by-text/" => "/can-nurse-practitioner-prescribe-antibiotics/",
        // Duplicate poison ivy plate retired (2026-10-29) — Chris: "Fix this please".
        // Kept /poison-ivy/ (the one with Search Console impressions). The old static
        // index.html stays on disk, so public_html/conditions/.htaccess fires this 301 first.
        "/conditions/poison-ivy-treatment/" => "/poison-ivy/",
    ];
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    $path = rtrim($path, "/") . "/";
    if (isset($redirects[$path])) {
        header("Cache-Control: no-cache, no-store, must-revalidate");
        header("Location: " . home_url($redirects[$path]), true, 301);
        exit;
    }
    // Leftover preview posts still 200 at ?p=ID even after the slug 301s.
    $preview_ids = [
        825 => "/pricing/",
        839 => "/ear-pain-after-swimming-swimmers-ear/",
        802 => "/conditions/",
    ];
    if (isset($_GET["p"])) {
        $pid = (int) $_GET["p"];
        if (isset($preview_ids[$pid])) {
            header("Cache-Control: no-cache, no-store, must-revalidate");
            header("Location: " . home_url($preview_ids[$pid]), true, 301);
            exit;
        }
    }
});
add_action("template_redirect", function() {
    if (is_author()) {
        wp_redirect(home_url("/about/"), 301);
        exit;
    }
});

// Yoast wpseo_sitemap_exclude_author filter empties content but still serves
// /author-sitemap.xml with HTTP 200, which Search Console reports as an error.
// Force 410 Gone so Google drops it from the index.
add_action("init", function() {
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    if ($path === "/author-sitemap.xml" || $path === "/author-sitemap1.xml") {
        status_header(410);
        header("Content-Type: text/plain; charset=UTF-8");
        echo "Gone";
        exit;
    }
}, 1);

// Blog removals (2026-10-17) — Chris approved: these posts are gone for good.
// Posts are set to draft in WP (not trashed); the URLs answer 410 Gone.
add_action("init", function() {
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    $path = rtrim((string) $path, "/") . "/";
    $gone = [
        "/sunburn-with-blisters-when-to-get-checked/",
        "/alpha-gal-syndrome-tick-bite-what-to-watch-for/",
    ];
    if (in_array($path, $gone, true)) {
        status_header(410);
        header("Cache-Control: no-cache, no-store, must-revalidate");
        header("Content-Type: text/plain; charset=UTF-8");
        echo "Gone";
        exit;
    }
}, 1);
