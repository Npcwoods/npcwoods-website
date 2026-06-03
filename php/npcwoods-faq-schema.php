<?php
/**
 * Plugin Name: NPCWoods SEO Fixes
 * Description: FAQ schema, 301 redirects, meta descriptions, canonical tags, noindex, and image alt text
 * Version: 5.0
 * Author: Chris Woods
 */

// ============================================================
// 0. ONE-TIME SETUP: Write canonical values to Yoast post meta
// ============================================================
add_action('init', 'npcwoods_setup_canonicals');
function npcwoods_setup_canonicals() {
    if (get_option('npcwoods_canonicals_set_v5')) return;
    $canonical_map = array(
        189 => 'https://npcwoods.com/uti-treatment/',
        190 => 'https://npcwoods.com/sinus-infection-treatment/',
        191 => 'https://npcwoods.com/strep-throat-ear-infection/'
    );
    foreach ($canonical_map as $pid => $url) {
        update_post_meta($pid, '_yoast_wpseo_canonical', $url);
    }
    update_option('npcwoods_canonicals_set_v5', true);
}

// ============================================================
// 0b. BLOG META REWRITES v3 (2026-06-01 — added recent sitemap audit gaps)
// Sets Yoast SEO title + meta description for blog posts.
// Titles ≤ 60 chars, descriptions ≤ 160 chars, no banned words.
// ============================================================
add_action('init', 'npcwoods_setup_blog_metas_v1');
function npcwoods_setup_blog_metas_v1() {
    if (get_option('npcwoods_blog_metas_set_v3')) return;
    $meta_map = array(
        // 15 existing blog posts
        432 => array('title' => 'Spring Allergies or Sinus Infection? How to Tell', 'desc' => "Pressure, drainage, or itchy eyes — how to tell allergies from a sinus infection. Text a licensed NP for \$59 flat when you're done guessing."),
        326 => array('title' => 'Paying Out of Pocket? Text an NP for $59 Flat', 'desc' => 'Sick and paying cash? $59 flat fee text visits with a licensed nurse practitioner. No paperwork, no waiting room, prescription to your pharmacy.'),
        470 => array('title' => 'Text vs. Video Telehealth: Which Actually Works?', 'desc' => "Text beats video for common conditions like UTIs and sinus infections. Here's why — and when video is the better call. \$59 flat at NPCWoods."),
        469 => array('title' => 'Can an NP Prescribe Antibiotics? State-by-State', 'desc' => "Yes — licensed nurse practitioners can prescribe antibiotics in all 50 states. Here's how scope of practice works and what NPCWoods treats for \$59."),
        462 => array('title' => 'What Is Async Telemedicine? How It Works', 'desc' => 'Async telemedicine is healthcare by text message. No scheduling, no video call — just a licensed NP reviewing your case. $59 flat visit explained.'),
        458 => array('title' => 'Urgent Care Prices 2026: What You Actually Pay', 'desc' => 'The real cost of urgent care in 2026 — without benefits coverage. Compare to $59 flat fee text visits for the conditions that fit telehealth.'),
        454 => array('title' => 'Do I Need Antibiotics for a Sinus Infection?', 'desc' => "Not every sinus infection needs antibiotics. Here's when they help, when they don't, and how a licensed NP decides for \$59 flat."),
        450 => array('title' => "Burning When I Pee? Here's What to Do Now", 'desc' => "Burning, urgency, constant trips — here's what's happening and how to get evaluated and treated in under an hour for \$59 at NPCWoods."),
        439 => array('title' => 'Is Text-Based Telehealth Actually Safe?', 'desc' => '7 signs a telehealth service is legitimate — licensing, named clinician, real review, and clear limits. $59 flat visits at NPCWoods explained.'),
        438 => array('title' => "What Can Telehealth Prescribe? (And What It Can't)", 'desc' => '8 conditions telehealth handles well and 5 situations that need in-person care. Written by a licensed nurse practitioner. $59 flat visits.'),
        435 => array('title' => 'Get UTI Antibiotics Online: Same-Day Explained', 'desc' => "Burning, urgency, running to the bathroom? A licensed NP can send UTI antibiotics to your pharmacy same-day for \$59 flat. Here's how."),
        427 => array('title' => 'Stop Popping Benadryl: It May Be a Sinus Infection', 'desc' => "Benadryl isn't always the answer — sometimes it's a sinus infection hiding as allergies. Here's how to tell, and \$59 flat help when you need it."),
        419 => array('title' => "Tooth Infection? Don't Wait for Monday", 'desc' => 'Throbbing tooth pain on a weekend? A licensed NP can prescribe antibiotics to buy you time until you see a dentist. $59 flat at NPCWoods.'),
        305 => array('title' => 'Telehealth vs. Urgent Care: Cost & Speed', 'desc' => "When telehealth beats urgent care — and the 4 times it doesn't. Real cost comparison, timing, and condition fit. \$59 flat visits at NPCWoods."),
        304 => array('title' => 'Do I Need to See Someone for a UTI?', 'desc' => "Sometimes a UTI clears up. Often it doesn't. Here's how to tell — and when to text a licensed NP for antibiotics for \$59 flat."),
        // 5 new blog posts (April 14)
        523 => array('title' => '7 Fast Ways to Handle a UTI Without Urgent Care', 'desc' => 'Burning, urgency, or pressure? Seven practical ways to handle a UTI fast without a waiting room. $59 flat text visit with a licensed NP at NPCWoods.'),
        524 => array('title' => "8 Reasons Patients Pick Text Telehealth for Cash", 'desc' => 'Paying out of pocket and sick? Eight reasons cash-pay text telehealth beats urgent care — flat $59 pricing, no paperwork, licensed NP review.'),
        525 => array('title' => '6 Infections Text Telehealth Treats Same-Day', 'desc' => 'UTI, sinus, ear, strep, tooth, and yeast infections — six common ones text telehealth handles well. When it fits, when it does not. $59 flat.'),
        526 => array('title' => '10 Questions to Ask Before an Online Health Visit', 'desc' => 'Cash-pay telehealth quality varies. These ten questions separate real clinical care from script-refill sites. $59 flat visits at NPCWoods.'),
        527 => array('title' => "Can I Get Strep Antibiotics Online? What's Legit", 'desc' => 'Short answer: yes, in a lot of cases. When text telehealth fits strep, when it does not, and the typical antibiotics used. $59 flat at NPCWoods.'),
        // Added 2026-04-14 — Tier 1 #2 from audit (yeast infection)
        534 => array('title' => 'Yeast Infection Treatment by Text: $59 Flat', 'desc' => 'Itching, burning, thick white discharge? A double board-certified NP can prescribe fluconazole same-day for $59 flat. When telehealth fits — and when it does not.'),
        // Added 2026-06-01 — recent sitemap audit gaps
        696 => array('title' => 'Red Eye After Swimming: Pink Eye or Irritation?', 'desc' => 'Red, irritated eye after swimming? How to tell pool irritation from pink eye, when to use drops, and when to text an NP for $59 flat.'),
        673 => array('title' => "Ear Pain After Swimming? Swimmer's Ear Signs", 'desc' => "Ear pain after swimming? Learn swimmer's ear signs, red flags, and when a $59 text visit with a licensed NP may fit."),
        668 => array('title' => 'Allergies or Sinus Infection? How to Tell', 'desc' => 'Congestion, pressure, sneezing, or drainage? How to tell allergies from sinus infection and when to text a licensed NP for $59 flat.'),
        730 => array('title' => 'Wet Bathing Suit Irritation or Yeast Infection?', 'desc' => 'Irritation after a wet bathing suit? Learn yeast infection clues, what else can mimic it, and when text-based care may fit for $59 flat.'),
        700 => array('title' => 'Hot Tub Rash After a Cabin Weekend?', 'desc' => 'Bumpy itchy rash after a hot tub or cabin weekend? What hot tub rash usually looks like, what to avoid, and when to get checked.'),
    );
    foreach ($meta_map as $pid => $m) {
        update_post_meta($pid, '_yoast_wpseo_title', $m['title']);
        update_post_meta($pid, '_yoast_wpseo_metadesc', $m['desc']);
    }
    update_option('npcwoods_blog_metas_set_v3', true);
}

// ============================================================
// 1. FAQ SCHEMA MARKUP (handles both dl/dt/dd AND h3/p formats)
// ============================================================
add_action('wp_footer', 'npcwoods_faq_schema');
function npcwoods_faq_schema() {
    if (!is_singular('page')) return;
    global $post;
    $content = $post->post_content;
    if (stripos($content, 'Frequently Asked') === false && stripos($content, 'Common Questions') === false) return;
    $faqs = array();
    preg_match_all('/<dt[^>]*>\s*<strong>(.*?)<\/strong>\s*<\/dt>\s*<dd>(.*?)<\/dd>/s', $content, $matches);
    if (!empty($matches[1])) {
        for ($i = 0; $i < count($matches[1]); $i++) {
            $q = wp_strip_all_tags(html_entity_decode($matches[1][$i]));
            $a = wp_strip_all_tags(html_entity_decode($matches[2][$i]));
            if (!empty($q) && !empty($a)) {
                $faqs[] = array('@type'=>'Question','name'=>$q,'acceptedAnswer'=>array('@type'=>'Answer','text'=>$a));
            }
        }
    }
    if (empty($faqs)) {
        $faq_pos = stripos($content, 'Frequently Asked');
        if ($faq_pos === false) $faq_pos = stripos($content, 'Common Questions');
        if ($faq_pos !== false) {
            $faq_section = substr($content, $faq_pos);
            $next_h2 = strpos($faq_section, '<h2', 10);
            if ($next_h2 !== false) $faq_section = substr($faq_section, 0, $next_h2);
            preg_match_all('/<h3[^>]*>(.*?)<\/h3>\s*<p>(.*?)<\/p>/s', $faq_section, $matches2);
            if (!empty($matches2[1])) {
                for ($i = 0; $i < count($matches2[1]); $i++) {
                    $q = wp_strip_all_tags(html_entity_decode($matches2[1][$i]));
                    $a = wp_strip_all_tags(html_entity_decode($matches2[2][$i]));
                    if (!empty($q) && !empty($a) && strpos($q, '?') !== false) {
                        $faqs[] = array('@type'=>'Question','name'=>$q,'acceptedAnswer'=>array('@type'=>'Answer','text'=>$a));
                    }
                }
            }
        }
    }
    if (empty($faqs)) return;
    $schema = array('@context'=>'https://schema.org','@type'=>'FAQPage','mainEntity'=>$faqs);
    echo '<script type="application/ld+json">'.json_encode($schema, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES).'</script>'."\n";
}

// ============================================================
// 2. 301 REDIRECTS
// ============================================================
add_action('template_redirect', 'npcwoods_301_redirects');
function npcwoods_301_redirects() {
    $path = rtrim(strtok($_SERVER['REQUEST_URI'], '?'), '/');
    if ($path === '/olivetree') {
        wp_redirect(home_url('/'), 301);
        exit;
    }
}

// ============================================================
// 3. META DESCRIPTIONS (only fills missing ones)
// ============================================================
add_filter('wpseo_metadesc', 'npcwoods_meta_descriptions');
function npcwoods_meta_descriptions($desc) {
    // Force-override homepage description (page 63) even if Yoast has one set
    if (is_singular('page') || is_front_page()) {
        global $post;
        if ($post && $post->ID == 63) {
            return 'NPCWoods Telemedicine — $59 text-based urgent care from a licensed Nurse Practitioner. No hassle, no waiting rooms. Same-day response. Text (480) 639-4722.';
        }
    }
    if (!empty($desc)) return $desc;
    if (!is_singular('page')) return $desc;
    global $post;
    $cities = array(
        // Arizona
        'phoenix-az'=>'Phoenix, AZ','tucson-az'=>'Tucson, AZ','mesa-az'=>'Mesa, AZ',
        'chandler-az'=>'Chandler, AZ','gilbert-az'=>'Gilbert, AZ','glendale-az'=>'Glendale, AZ',
        'scottsdale-az'=>'Scottsdale, AZ','peoria-az'=>'Peoria, AZ','tempe-az'=>'Tempe, AZ','surprise-az'=>'Surprise, AZ',
        // Georgia
        'atlanta-ga'=>'Atlanta, GA','savannah-ga'=>'Savannah, GA','augusta-ga'=>'Augusta, GA',
        'columbus-ga'=>'Columbus, GA','athens-ga'=>'Athens, GA',
        // North Carolina
        'charlotte-nc'=>'Charlotte, NC','raleigh-nc'=>'Raleigh, NC','durham-nc'=>'Durham, NC',
        'greensboro-nc'=>'Greensboro, NC','wilmington-nc'=>'Wilmington, NC'
    );
    $descriptions = array(
        63=>'NPCWoods offers $59 telemedicine visits by text message. No hassle, no video calls, no waiting rooms. Treat UTIs, sinus infections, strep, ED and more. Licensed in AZ, GA, NC.',
        184=>'Online urgent care for UTIs, sinus infections, strep throat, ear infections, and ED. $59 flat fee per visit. Text-based telemedicine — no paperwork, no appointments needed.',
        192=>'Online ear infection treatment for $59. A licensed NP evaluates your symptoms by text and sends prescriptions to your pharmacy. No video call, no hassle.',
        198=>'Affordable telemedicine in Arizona — $59 flat fee for urgent care by text message. Treat UTIs, sinus infections, strep, and ED from home. No paperwork.',
        3=>'NPCWoods Telemedicine privacy policy.',
        252=>'Affordable telemedicine in Georgia for $59. Text a licensed NP, get diagnosed, and pick up your prescription at a local pharmacy. No hassle, no video call.',
        253=>'Affordable telemedicine in North Carolina for $59. Text a licensed NP, get diagnosed, and pick up your prescription at a local pharmacy. No hassle, no video call.');
    if (isset($descriptions[$post->ID])) return $descriptions[$post->ID];
    if (isset($cities[$post->post_name])) {
        $city = $cities[$post->post_name];
        $parent = get_post($post->post_parent);
        if ($parent) {
            $ps = $parent->post_name;
            if (strpos($ps,'uti')!==false) return "UTI treatment in {$city} for \$59. Text your symptoms to a licensed NP and get antibiotics sent to your local pharmacy today. No hassle, no paperwork.";
            if (strpos($ps,'sinus')!==false) return "Sinus infection treatment in {$city} for \$59. Get evaluated by a licensed NP via text and pick up your prescription same day. No paperwork, no waiting rooms.";
            if (strpos($ps,'strep')!==false) return "Strep throat and ear infection treatment in {$city} for \$59. Text a board-certified NP, get diagnosed, and pick up your prescription locally.";
            if (strpos($ps,'ed')!==false) return "Discreet ED treatment in {$city} for \$59. A licensed Nurse Practitioner evaluates you by text and sends your prescription privately. No hassle, no paperwork.";
        }
    }
    return $desc;
}

// ============================================================
// 4. CANONICAL OVERRIDES — Output buffer approach as nuclear option
// ============================================================
add_filter('wpseo_canonical', 'npcwoods_canonical_overrides', 20);
function npcwoods_canonical_overrides($canonical) {
    if (!is_singular('page')) return $canonical;
    global $post;
    $map = array(
        189 => 'https://npcwoods.com/uti-treatment/',
        190 => 'https://npcwoods.com/sinus-infection-treatment/',
        191 => 'https://npcwoods.com/strep-throat-ear-infection/'
    );
    return isset($map[$post->ID]) ? $map[$post->ID] : $canonical;
}

// Output buffer to catch and replace canonical tags on duplicate pages
add_action('template_redirect', 'npcwoods_start_canonical_buffer', 0);
function npcwoods_start_canonical_buffer() {
    if (!is_singular('page')) return;
    global $post;
    if (!$post || !in_array($post->ID, array(189, 190, 191))) return;
    ob_start('npcwoods_replace_canonical');
}

function npcwoods_replace_canonical($html) {
    global $post;
    $map = array(
        189 => 'https://npcwoods.com/uti-treatment/',
        190 => 'https://npcwoods.com/sinus-infection-treatment/',
        191 => 'https://npcwoods.com/strep-throat-ear-infection/'
    );
    if (!$post || !isset($map[$post->ID])) return $html;
    $target = $map[$post->ID];
    // Replace any canonical link tag
    $html = preg_replace(
        '/<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*\/?>/i',
        '<link rel="canonical" href="' . esc_url($target) . '" />',
        $html
    );
    return $html;
}

// ============================================================
// 5. NOINDEX PRIVACY POLICY
// ============================================================
add_filter('wpseo_robots_array', 'npcwoods_noindex_pages');
function npcwoods_noindex_pages($robots) {
    if (is_page(3)) { $robots['index'] = 'noindex'; }
    return $robots;
}

// ============================================================
// 6. DEFAULT ALT TEXT
// ============================================================
add_filter('wp_get_attachment_image_attributes', 'npcwoods_default_alt_text', 10, 3);
function npcwoods_default_alt_text($attr, $attachment, $size) {
    if (empty($attr['alt'])) {
        $title = get_the_title($attachment->ID);
        $attr['alt'] = !empty($title) ? $title.' - NPCWoods Telemedicine' : 'NPCWoods Telemedicine - $59 Online Urgent Care';
    }
    // Add lazy loading to all images except the first one (LCP)
    if (!isset($GLOBALS['npcwoods_img_count'])) $GLOBALS['npcwoods_img_count'] = 0;
    $GLOBALS['npcwoods_img_count']++;
    if ($GLOBALS['npcwoods_img_count'] > 1 && !isset($attr['loading'])) {
        $attr['loading'] = 'lazy';
    }
    return $attr;
}

// ============================================================
// 7. PRECONNECT HINTS FOR SPEED
// ============================================================
add_action('wp_head', 'npcwoods_speed_hints', 1);
function npcwoods_speed_hints() {
    echo '<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin />' . "\n";
    echo '<link rel="dns-prefetch" href="https://fonts.googleapis.com" />' . "\n";
}

// ============================================================
// 8. HOMEPAGE SEO OVERRIDES (page 63)
//    Removes "insurance" from all meta tags (brand rule #4)
// ============================================================

add_filter('wpseo_title', function($title) {
    if (is_front_page() || (is_page() && get_the_ID() == 63)) {
        return 'NPCWoods Telemedicine — $59 Online Urgent Care | No Hassle';
    }
    return $title;
}, 20);

add_filter('wpseo_opengraph_title', function($title) {
    if (is_front_page() || (is_page() && get_the_ID() == 63)) {
        return 'NPCWoods Telemedicine — $59 Online Urgent Care';
    }
    return $title;
}, 20);

add_filter('wpseo_opengraph_desc', function($desc) {
    if (is_front_page() || (is_page() && get_the_ID() == 63)) {
        return 'See a real Nurse Practitioner from home — $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.';
    }
    return $desc;
}, 20);

add_filter('wpseo_twitter_title', function($title) {
    if (is_front_page() || (is_page() && get_the_ID() == 63)) {
        return 'NPCWoods Telemedicine — $59 Online Urgent Care';
    }
    return $title;
}, 20);

add_filter('wpseo_twitter_description', function($desc) {
    if (is_front_page() || (is_page() && get_the_ID() == 63)) {
        return 'See a real Nurse Practitioner from home — $59 flat fee, no hassle. Text-based urgent care for UTI, sinus infections, strep, ED, and more.';
    }
    return $desc;
}, 20);

// ============================================================
// 9. SITEMAP CLEANUP
//    Remove redirecting pages + disable author sitemap
// ============================================================

// Exclude pages that redirect, duplicate, orphan, or are city pages (crawl budget strategy)
add_filter('wpseo_exclude_from_sitemap_by_post_ids', function() {
    return array(
        // 301 redirects
        327,  // mesa-uti-treatment (redirects to /uti-treatment/mesa-az/)
        333,  // scottsdale-uti-treatment (redirects to /uti-treatment/scottsdale-az/)
        328,  // albuquerque-uti-treatment (redirects to /uti-treatment/albuquerque-nm/)
        405,  // pharmacy-info (redirects to /pharmacy/)
        406,  // states (redirects to homepage)
        192,  // /ear-infection/ redirects to /ear-infection-treatment/
        8,    // /strep-throat-ear-infection/ (legacy hub, redirects to /strep-throat-treatment/)
        // Duplicate pages (canonical points elsewhere)
        189,  // /uti/ → canonical to /uti-treatment/
        190,  // /sinus/ → canonical to /sinus-infection-treatment/
        191,  // /strep/ → canonical to /strep-throat-ear-infection/
        310,  // /patient-experience-2/ legacy duplicate of /patient-experience/
        // Orphan/junk pages
        56,   // /home/phoenix-telemedicine/ (orphan, not linked anywhere)
        58,   // /tucson-telemedicine/ (orphan, no redirect configured)
        329,  // /blog-burning-when-you-pee-albuquerque/ static orphan with mismatched canonical
        // Front page is already emitted separately by Yoast, so exclude the page object
        // to prevent https://npcwoods.com/ from appearing twice in page-sitemap.xml.
        63,   // home/front page duplicate
        // Noindexed pages (shouldn't be in sitemap)
        3,    // privacy-policy (noindexed)
        654,  // /review/ (noindexed review funnel)
        674,  // /pay/ (noindexed payment handoff)

        // ============================================================
        // PAID-ONLY NOINDEX CLONES (not in sitemap; only paid traffic lands here)
        // ============================================================
        698,  // /uti-care/ paid Google + Facebook clone (noindexed)

        // ============================================================
        // CITY PAGES — temporarily excluded to focus crawl budget
        // on 66 core pages. Re-add once domain authority grows.
        // Pages still work if visited directly, just not in sitemap.
        // ============================================================
        // UTI Treatment city pages (AZ) - Mesa (13), Scottsdale (17), Surprise (20) re-added
        11, 12, 14, 15, 16, 18, 19,
        // UTI Treatment city pages (GA/NC) + Albuquerque - Atlanta (264), Charlotte (284), Albuquerque (411) re-added
        268, 272, 276, 280, 288, 292, 296, 300,
        // Sinus Infection Treatment city pages (AZ) - Phoenix (21) re-added; Mesa (23) excluded until served correctly
        22, 23, 24, 25, 26, 27, 28, 29, 30,
        // Sinus Infection Treatment city pages (GA/NC)
        265, 269, 273, 277, 281, 285, 289, 293, 297, 301,
        // Strep Throat/Ear Infection city pages (AZ)
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        // Strep Throat/Ear Infection city pages (GA/NC)
        266, 270, 274, 278, 282, 286, 290, 294, 298, 302,
        // ED Treatment city pages (AZ)
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
        // ED Treatment city pages (GA/NC)
        267, 271, 275, 279, 283, 287, 291, 295, 299, 303,
    );
});

// Disable author sitemap entirely (leaks WP admin username)
add_filter('wpseo_sitemap_exclude_author', '__return_true');
