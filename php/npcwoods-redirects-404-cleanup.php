<?php
/**
 * Plugin Name: NPCWoods 301 Redirects — 404 Cleanup (2026-04-22)
 * Description: Fixes orphan 4XX URLs flagged by Ahrefs Site Audit.
 *              Separate file from npcwoods-redirects.php so the original stays
 *              a clean pristine snapshot and this batch is trivially revertable.
 *              Slug sets are disjoint from npcwoods-redirects.php — safe to run both.
 */
add_action("init", function() {
    $redirects = [
        // Bucket A — flat-slug city × condition 404s → condition hub / state hub
        // AZ strep (→ strep hub)
        "/phoenix-az-strep/"                => "/strep-throat-treatment/",
        "/chandler-az-strep/"               => "/strep-throat-treatment/",
        "/tempe-az-strep/"                  => "/strep-throat-treatment/",
        "/glendale-az-strep/"               => "/strep-throat-treatment/",
        "/surprise-az-strep/"               => "/strep-throat-treatment/",
        "/tucson-az-strep/"                 => "/strep-throat-treatment/",
        "/peoria-az-strep/"                 => "/strep-throat-treatment/",
        "/mesa-az-strep/"                   => "/strep-throat-treatment/",
        // AZ UTI (→ UTI hub; no nested page exists for these cities)
        "/phoenix-uti-treatment/"           => "/uti-treatment/",
        // AZ sinus (→ sinus hub)
        "/phoenix-sinus-infection/"         => "/sinus-infection-treatment/",
        "/mesa-sinus-infection/"            => "/sinus-infection-treatment/",
        "/scottsdale-sinus-infection/"      => "/sinus-infection-treatment/",
        "/tucson-sinus-infection/"          => "/sinus-infection-treatment/",
        "/surprise-sinus-infection/"        => "/sinus-infection-treatment/",
        "/tucson-az-sinus/"                 => "/sinus-infection-treatment/",
        // AZ telemedicine (→ AZ state hub)
        "/mesa-telemedicine/"               => "/arizona-telemedicine/",
        "/scottsdale-telemedicine/"         => "/arizona-telemedicine/",
        "/gilbert-telemedicine/"            => "/arizona-telemedicine/",
        "/glendale-az-telemedicine/"        => "/arizona-telemedicine/",
        "/glendale-telemedicine/"           => "/arizona-telemedicine/",
        "/tempe-telemedicine/"              => "/arizona-telemedicine/",
        "/chandler-telemedicine/"           => "/arizona-telemedicine/",
        "/surprise-telemedicine/"           => "/arizona-telemedicine/",
        "/peoria-az-telemedicine/"          => "/arizona-telemedicine/",
        // AZ ED (→ ED hub)
        "/tucson-az-ed/"                    => "/ed-treatment/",
        // AZ strep gap fill
        "/scottsdale-az-strep/"             => "/strep-throat-treatment/",
        // NM UTI (→ UTI hub)
        "/santa-fe-uti-treatment/"          => "/uti-treatment/",
        "/rio-rancho-uti-treatment/"        => "/uti-treatment/",
        "/farmington-uti-treatment/"        => "/uti-treatment/",
        // NM sinus (→ sinus hub)
        "/albuquerque-sinus-infection/"     => "/sinus-infection-treatment/",
        "/santa-fe-sinus-infection/"        => "/sinus-infection-treatment/",
        "/rio-rancho-sinus-infection/"      => "/sinus-infection-treatment/",
        "/las-cruces-sinus-infection/"      => "/sinus-infection-treatment/",
        "/farmington-sinus-infection/"      => "/sinus-infection-treatment/",
        // NM telemedicine (→ NM state hub)
        "/santa-fe-telemedicine/"           => "/new-mexico-telemedicine/",
        "/rio-rancho-telemedicine/"         => "/new-mexico-telemedicine/",
        "/farmington-telemedicine/"         => "/new-mexico-telemedicine/",
        "/las-cruces-telemedicine/"         => "/new-mexico-telemedicine/",
        "/roswell-telemedicine/"            => "/new-mexico-telemedicine/",
        "/albuquerque-telemedicine/"        => "/new-mexico-telemedicine/",
        // GA UTI (→ UTI hub; no GA state hub)
        "/dalton-uti-treatment/"            => "/uti-treatment/",
        "/gainesville-ga-uti-treatment/"    => "/uti-treatment/",
        "/augusta-uti-treatment/"           => "/uti-treatment/",
        "/athens-uti-treatment/"            => "/uti-treatment/",
        // GA sinus (→ sinus hub)
        "/atlanta-sinus-infection/"         => "/sinus-infection-treatment/",
        "/dalton-sinus-infection/"          => "/sinus-infection-treatment/",
        "/augusta-sinus-infection/"         => "/sinus-infection-treatment/",
        "/athens-sinus-infection/"          => "/sinus-infection-treatment/",
        "/gainesville-ga-sinus-infection/"  => "/sinus-infection-treatment/",
        // NC UTI (→ UTI hub; no NC state hub)
        "/charlotte-uti-treatment/"         => "/uti-treatment/",
        "/asheville-uti-treatment/"         => "/uti-treatment/",
        "/hickory-uti-treatment/"           => "/uti-treatment/",
        "/hendersonville-uti-treatment/"    => "/uti-treatment/",
        "/boone-uti-treatment/"             => "/uti-treatment/",
        // NC sinus (→ sinus hub)
        "/charlotte-sinus-infection/"       => "/sinus-infection-treatment/",
        "/hickory-sinus-infection/"         => "/sinus-infection-treatment/",
        "/hendersonville-sinus-infection/"  => "/sinus-infection-treatment/",
        // Conditions index slug drift (plural → singular)
        "/conditions/skin-infections/"      => "/learn/skin-infection/",
        // Bucket B — /learn/ slug drift (3 rules)
        "/learn/respiratory-infection/"     => "/learn/bronchitis/",
        "/learn/cold-flu/"                  => "/learn/covid-flu/",
        "/learn/hives/"                     => "/learn/allergic-reaction/",
        "/learn/acne/"                      => "/learn/skin-infection/",
        "/learn/abscesses/"                 => "/dental-pain/",
        // Bucket C — orphan stubs (no matching page in WP)
        "/contact/"                         => "/about/",
    ];
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    $path = rtrim($path, "/") . "/";
    if (isset($redirects[$path])) {
        header("Cache-Control: no-cache, no-store, must-revalidate");
        header("Location: " . home_url($redirects[$path]), true, 301);
        exit;
    }
});
