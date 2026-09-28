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
        "/blog/burning-when-you-pee-albuquerque/" => "/blog-burning-when-you-pee-albuquerque/",
        "/experience/"               => "/patient-experience/",
        "/ear-infection/"            => "/ear-infection-treatment/",
        "/cost-savings-preview/"     => "/cost-savings-convenience/",
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
        825 => "/cost-savings-convenience/",
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
//
// /sitemap.xml is a Yoast 301 to /sitemap_index.xml on the apex host only.
// www.npcwoods.com/sitemap.xml is a real WordPress 404, so checkers that hit
// www first report a missing sitemap. Send every host to the apex Yoast index.
// A 301 here is success, not a missing file.
add_action("init", function() {
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    if ($path === "/author-sitemap.xml" || $path === "/author-sitemap1.xml") {
        status_header(410);
        header("Content-Type: text/plain; charset=UTF-8");
        echo "Gone";
        exit;
    }
    if ($path === "/sitemap.xml" || $path === "/sitemap.xml/") {
        header("Cache-Control: no-cache, no-store, must-revalidate");
        header("Location: https://npcwoods.com/sitemap_index.xml", true, 301);
        exit;
    }
}, 1);
