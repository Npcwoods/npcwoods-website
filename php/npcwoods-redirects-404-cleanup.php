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
        "/phoenix-uti-treatment/"           => "/uti-treatment/phoenix-az/",
        // AZ sinus (→ sinus hub / city page when a real draft exists)
        "/phoenix-az-sinus/"                => "/sinus-infection-treatment/phoenix-az/",
        "/phoenix-sinus-infection/"         => "/sinus-infection-treatment/phoenix-az/",
        "/mesa-sinus-infection/"            => "/sinus-infection-treatment/mesa-az/",
        "/chandler-sinus-infection/"        => "/sinus-infection-treatment/chandler-az/",
        "/scottsdale-sinus-infection/"      => "/sinus-infection-treatment/scottsdale-az/",
        "/tucson-sinus-infection/"          => "/sinus-infection-treatment/tucson-az/",
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
        // Bucket D — leftover nested city kids-menus (2026-08-29). Take the
        // seats down. Arrow to the matching condition bar, not a 404.
        "/ed-treatment/athens-ga/" => "/ed-treatment/",
        "/ed-treatment/augusta-ga/" => "/ed-treatment/",
        "/ed-treatment/chandler-az/" => "/ed-treatment/",
        "/ed-treatment/columbus-ga/" => "/ed-treatment/",
        "/ed-treatment/durham-nc/" => "/ed-treatment/",
        "/ed-treatment/gilbert-az/" => "/ed-treatment/",
        "/ed-treatment/glendale-az/" => "/ed-treatment/",
        "/ed-treatment/greensboro-nc/" => "/ed-treatment/",
        "/ed-treatment/mesa-az/" => "/ed-treatment/",
        "/ed-treatment/peoria-az/" => "/ed-treatment/",
        "/ed-treatment/phoenix-az/" => "/ed-treatment/",
        "/ed-treatment/raleigh-nc/" => "/ed-treatment/",
        "/ed-treatment/savannah-ga/" => "/ed-treatment/",
        "/ed-treatment/scottsdale-az/" => "/ed-treatment/",
        "/ed-treatment/surprise-az/" => "/ed-treatment/",
        "/ed-treatment/tempe-az/" => "/ed-treatment/",
        "/ed-treatment/tucson-az/" => "/ed-treatment/",
        "/ed-treatment/wilmington-nc/" => "/ed-treatment/",
        "/sinus-infection-treatment/athens-ga/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/augusta-ga/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/columbus-ga/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/durham-nc/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/gilbert-az/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/glendale-az/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/greensboro-nc/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/peoria-az/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/raleigh-nc/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/savannah-ga/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/surprise-az/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/tempe-az/" => "/sinus-infection-treatment/",
        "/sinus-infection-treatment/wilmington-nc/" => "/sinus-infection-treatment/",
        "/strep-throat-ear-infection/athens-ga/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/augusta-ga/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/chandler-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/columbus-ga/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/durham-nc/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/gilbert-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/glendale-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/greensboro-nc/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/mesa-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/peoria-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/phoenix-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/raleigh-nc/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/savannah-ga/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/scottsdale-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/surprise-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/tempe-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/tucson-az/" => "/strep-throat-treatment/",
        "/strep-throat-ear-infection/wilmington-nc/" => "/strep-throat-treatment/",
        "/uti-treatment/athens-ga/" => "/uti-treatment/",
        "/uti-treatment/columbus-ga/" => "/uti-treatment/",
        "/uti-treatment/durham-nc/" => "/uti-treatment/",
        "/uti-treatment/greensboro-nc/" => "/uti-treatment/",
        "/uti-treatment/peoria-az/" => "/uti-treatment/",
        "/uti-treatment/wilmington-nc/" => "/uti-treatment/",
    ];
    $path = parse_url($_SERVER["REQUEST_URI"], PHP_URL_PATH);
    $path = rtrim($path, "/") . "/";
    if (isset($redirects[$path])) {
        header("Cache-Control: no-cache, no-store, must-revalidate");
        header("Location: " . home_url($redirects[$path]), true, 301);
        exit;
    }
});
