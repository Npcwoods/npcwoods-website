<?php
/**
 * Plugin Name: NPCWoods E-E-A-T Signals
 * Description: Strengthens clinician attribution, trust messaging, and entity consistency across medical content.
 * Version: 1.0
 * Author: Chris Woods
 */

function npcwoods_clinician_profile() {
    return array(
        'name' => 'Chris Woods, MSN, APRN, FNP-C',
        'short_name' => 'Chris Woods',
        'title' => 'Licensed Nurse Practitioner',
        'about_url' => home_url('/about/'),
        'disclaimer_url' => home_url('/medical-disclaimer/'),
        'privacy_url' => home_url('/privacy-policy/'),
        'terms_url' => home_url('/terms-of-service/'),
        'phone_href' => 'sms:4806394722',
        'phone_label' => '(480) 639-4722',
        'email' => 'cwoods@npcwoods.com',
        'headshot' => 'https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png',
        'npi' => '1285125468',
        'npi_url' => 'https://npiregistry.cms.hhs.gov/',
        'legitscript_url' => 'https://www.legitscript.com/websites/?checker_keywords=npcwoods.com',
        'organization_id' => home_url('/#medical-business'),
        'person_id' => home_url('/#chris-woods'),
        'states' => 'AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT',
    );
}

add_filter('author_link', function($link) {
    return home_url('/about/');
}, 10, 1);

add_filter('pre_get_avatar_data', function($args, $id_or_email) {
    $profile = npcwoods_clinician_profile();
    $args['url'] = $profile['headshot'];
    $args['found_avatar'] = true;
    return $args;
}, 10, 2);

add_action('wp_head', function() {
    // Fire on homepage, all WordPress pages, and all blog posts.
    // Article schema only emits for actual posts; Person + MedicalBusiness emit everywhere.
    $is_post = is_singular('post');
    $is_page = is_singular('page');
    $is_home = is_front_page();
    if (!$is_post && !$is_page && !$is_home) return;

    $profile = npcwoods_clinician_profile();
    $post_id = get_queried_object_id();
    $permalink = $is_home ? home_url('/') : ($post_id ? get_permalink($post_id) : home_url('/'));

    echo '<link rel="author" href="' . esc_url($profile['about_url']) . '" />' . "\n";
    // cite-as tells AI crawlers which URL to attribute when citing this content
    echo '<link rel="cite-as" href="' . esc_url($permalink) . '" />' . "\n";

    $person = array(
        '@type' => 'Person',
        '@id' => $profile['person_id'],
        'name' => $profile['short_name'],
        'url' => $profile['about_url'],
        'description' => 'Chris Woods is a Licensed Nurse Practitioner and founder of NPCWoods Telemedicine. He personally reviews every case and every medical article on the site.',
        'honorificSuffix' => 'MSN, APRN, FNP-C',
        'hasCredential' => array(
            '@type' => 'EducationalOccupationalCredential',
            'credentialCategory' => 'certification',
            'name' => 'MSN, APRN, FNP-C',
        ),
        'identifier' => array(
            '@type' => 'PropertyValue',
            'propertyID' => 'NPI',
            'value' => isset($profile['npi']) ? $profile['npi'] : '1285125468',
        ),
        'sameAs' => array(
            'https://npiregistry.cms.hhs.gov/provider-view/1285125468',
            'https://www.healthgrades.com/providers/christopher-woods-xynt5wl',
            'https://doctor.webmd.com/doctor/christopher-woods-7b55e933-62ef-4d7b-975c-9cfc40eb3ad8-overview',
            'https://www.facebook.com/npcwoods',
        ),
        'medicalSpecialty' => 'FamilyPractice',
        'jobTitle' => 'Licensed Nurse Practitioner',
        'image' => $profile['headshot'],
        'worksFor' => array('@id' => $profile['organization_id']),
    );

    $business = array(
        '@type' => 'MedicalBusiness',
        '@id' => $profile['organization_id'],
        'name' => 'NPCWoods Telemedicine',
        'url' => home_url('/'),
        'description' => 'Text-based telemedicine visits from a licensed nurse practitioner for a flat $59 fee.',
        'priceRange' => '$59',
        'telephone' => '+14806394722',
        'email' => $profile['email'],
        'image' => $profile['headshot'],
        'medicalSpecialty' => 'FamilyPractice',
        'founder' => array('@id' => $profile['person_id']),
        'employee' => array('@id' => $profile['person_id']),
        'areaServed' => array(
            array('@type' => 'State', 'name' => 'Arizona'),
            array('@type' => 'State', 'name' => 'Colorado'),
            array('@type' => 'State', 'name' => 'Georgia'),
            array('@type' => 'State', 'name' => 'Idaho'),
            array('@type' => 'State', 'name' => 'Iowa'),
            array('@type' => 'State', 'name' => 'Montana'),
            array('@type' => 'State', 'name' => 'Nevada'),
            array('@type' => 'State', 'name' => 'New Mexico'),
            array('@type' => 'State', 'name' => 'North Carolina'),
            array('@type' => 'State', 'name' => 'Oregon'),
            array('@type' => 'State', 'name' => 'Utah'),
        ),
        // Ratings live on the Google Business Profile — self-hosted review markup violates Google policy
        'address' => array(
            '@type' => 'PostalAddress',
            'addressLocality' => 'Scottsdale',
            'addressRegion' => 'AZ',
            'addressCountry' => 'US',
        ),
        'paymentAccepted' => 'Cash, Credit Card, HSA, FSA',
        'makesOffer' => array(
            '@type' => 'Offer',
            'name' => 'Async telemedicine visit',
            'price' => '59.00',
            'priceCurrency' => 'USD',
        ),
    );

    $graph = array($person, $business);

    if ($is_post && $post_id) {
        $headline = wp_strip_all_tags(get_the_title($post_id));
        $description = wp_strip_all_tags(get_the_excerpt($post_id));
        $description = $description ? $description : 'Clinician-reviewed medical guidance from NPCWoods Telemedicine.';
        $published = get_the_date(DATE_W3C, $post_id);
        $modified = get_the_modified_date(DATE_W3C, $post_id);

        $graph[] = array(
            '@type' => 'Article',
            '@id' => $permalink . '#npcwoods-clinical-review',
            'mainEntityOfPage' => $permalink,
            'headline' => $headline,
            'description' => $description,
            'datePublished' => $published,
            'dateModified' => $modified,
            'author' => array('@id' => $profile['person_id']),
            'publisher' => array('@id' => $profile['organization_id']),
            'speakable' => array(
                '@type' => 'SpeakableSpecification',
                'cssSelector' => array('h1', '.quick-answer', 'h2'),
            ),
        );
    } elseif ($is_home) {
        // Homepage gets WebSite schema with SpeakableSpecification for voice/AI surfaces
        // and a SearchAction so Google can render the sitelinks search box for branded queries.
        $graph[] = array(
            '@type' => 'WebSite',
            '@id' => home_url('/#website'),
            'url' => home_url('/'),
            'name' => 'NPCWoods Telemedicine',
            'description' => 'Text-based urgent care from a licensed Nurse Practitioner. Flat $59. No paperwork. Same-day response.',
            'publisher' => array('@id' => $profile['organization_id']),
            'potentialAction' => array(
                '@type' => 'SearchAction',
                'target' => array(
                    '@type' => 'EntryPoint',
                    'urlTemplate' => home_url('/?s={search_term_string}'),
                ),
                'query-input' => 'required name=search_term_string',
            ),
            'speakable' => array(
                '@type' => 'SpeakableSpecification',
                'cssSelector' => array('h1', 'h2', '.hero-subtitle'),
            ),
        );
    } elseif ($is_page && $post_id) {
        // WordPress page (state landing pages, etc.) — emit MedicalWebPage schema
        $headline = wp_strip_all_tags(get_the_title($post_id));
        $graph[] = array(
            '@type' => 'MedicalWebPage',
            '@id' => $permalink . '#webpage',
            'url' => $permalink,
            'name' => $headline,
            'isPartOf' => array('@id' => home_url('/#website')),
            'about' => array('@id' => $profile['organization_id']),
            'reviewedBy' => array('@id' => $profile['person_id']),
            'lastReviewed' => get_the_modified_date(DATE_W3C, $post_id),
            'speakable' => array(
                '@type' => 'SpeakableSpecification',
                'cssSelector' => array('h1', 'h2'),
            ),
        );
    }

    $schema = array(
        '@context' => 'https://schema.org',
        '@graph' => $graph,
    );

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}, 30);

add_action('wp_head', function() {
    if (!is_singular('post')) return;
    ?>
    <style>
        .npc-post-trust-block {
            margin: 28px auto 28px;
            max-width: 760px;
            border: 1px solid #dbe5f5;
            border-radius: 24px;
            background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
            box-shadow: 0 18px 40px rgba(37, 99, 235, 0.08);
            overflow: hidden;
        }
        .npc-post-trust-header {
            padding: 22px 24px 18px;
            border-bottom: 1px solid #e5edf8;
        }
        .npc-post-trust-kicker {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding: 6px 12px;
            border-radius: 999px;
            background: #e8f1ff;
            color: #1d4ed8;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .npc-post-trust-header h2 {
            margin: 0 0 10px;
            color: #13233f;
            font-size: clamp(1.15rem, 2vw, 1.45rem);
            line-height: 1.25;
        }
        .npc-post-trust-header p {
            margin: 0;
            color: #4b5d7a;
            font-size: 0.98rem;
            line-height: 1.65;
        }
        .npc-post-trust-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            padding: 18px 24px 20px;
        }
        .npc-post-trust-card {
            padding: 16px 18px;
            border-radius: 18px;
            background: #f6f9fe;
            border: 1px solid #e4ebf7;
        }
        .npc-post-trust-label {
            margin: 0 0 6px;
            color: #1e40af;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .npc-post-trust-card p {
            margin: 0;
            color: #25364f;
            font-size: 0.94rem;
            line-height: 1.55;
        }
        .npc-post-trust-links {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 0 24px 22px;
        }
        .npc-post-trust-links a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            border-radius: 999px;
            background: #13233f;
            color: #ffffff;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .npc-post-trust-links a.npc-post-trust-secondary {
            background: #eef4ff;
            color: #1e3a8a;
        }
        .npc-related-care-links {
            padding: 0 24px 24px;
        }
        .npc-related-care-links h3 {
            margin: 0 0 10px;
            color: #13233f;
            font-size: 0.95rem;
            font-weight: 700;
        }
        .npc-related-care-links ul {
            margin: 0;
            padding-left: 18px;
            color: #4b5d7a;
        }
        .npc-related-care-links li {
            margin-bottom: 8px;
        }
        .npc-related-care-links a {
            color: #1d4ed8;
        }
        @media (max-width: 700px) {
            .npc-post-trust-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    <?php
}, 25);

function npcwoods_related_resources_for_post($post) {
    $resources = array();
    $haystack = strtolower($post->post_title . ' ' . wp_strip_all_tags($post->post_content));

    if (strpos($haystack, 'uti') !== false) {
        $resources[] = array('url' => home_url('/learn/uti/'), 'label' => 'Read the UTI guide');
        $resources[] = array('url' => home_url('/uti-treatment/'), 'label' => 'See how NPCWoods treats UTIs');
        $resources[] = array('url' => home_url('/medications/nitrofurantoin/'), 'label' => 'Review nitrofurantoin basics');
    }

    if (strpos($haystack, 'sinus') !== false || strpos($haystack, 'allerg') !== false) {
        $resources[] = array('url' => home_url('/learn/sinus-infection/'), 'label' => 'Compare allergy symptoms vs sinus infection');
        $resources[] = array('url' => home_url('/sinus-infection-treatment/'), 'label' => 'See treatment options for sinus symptoms');
    }

    if (strpos($haystack, 'tooth') !== false || strpos($haystack, 'dental') !== false) {
        $resources[] = array('url' => home_url('/learn/tooth-infection/'), 'label' => 'Read the tooth infection guide');
        $resources[] = array('url' => home_url('/dental-pain/'), 'label' => 'See when telehealth can help dental pain');
    }

    if (strpos($haystack, 'telehealth') !== false || strpos($haystack, 'urgent care') !== false) {
        $resources[] = array('url' => home_url('/how-it-works/'), 'label' => 'Learn how text-based telemedicine works');
        $resources[] = array('url' => home_url('/telehealth-vs-urgent-care/'), 'label' => 'Compare telehealth vs urgent care');
    }

    $resources[] = array('url' => home_url('/about/'), 'label' => 'Meet Chris Woods and verify credentials');
    $resources[] = array('url' => home_url('/medical-disclaimer/'), 'label' => 'Read the medical disclaimer');

    $unique = array();
    $seen = array();
    foreach ($resources as $resource) {
        if (isset($seen[$resource['url']])) continue;
        if (untrailingslashit($resource['url']) === untrailingslashit(get_permalink($post))) continue;
        $seen[$resource['url']] = true;
        $unique[] = $resource;
    }

    return array_slice($unique, 0, 5);
}

add_filter('the_content', function($content) {
    if (is_admin() || !is_singular('post') || !in_the_loop() || !is_main_query()) {
        return $content;
    }

    if (strpos($content, 'npc-post-trust-block') !== false) {
        return $content;
    }

    $profile = npcwoods_clinician_profile();
    $post = get_post();
    if (!$post) return $content;

    $published = get_the_date('F j, Y', $post);
    $updated = get_the_modified_date('F j, Y', $post);
    $related = npcwoods_related_resources_for_post($post);

    $related_markup = '';
    if (!empty($related)) {
        $items = '';
        foreach ($related as $resource) {
            $items .= '<li><a href="' . esc_url($resource['url']) . '">' . esc_html($resource['label']) . '</a></li>';
        }
        $related_markup = '<div class="npc-related-care-links"><h3>Helpful next steps</h3><ul>' . $items . '</ul></div>';
    }

    $trust = '<section class="npc-post-trust-block" aria-label="Medical review details">'
        . '<div class="npc-post-trust-header">'
        . '<div class="npc-post-trust-kicker">Clinician reviewed</div>'
        . '<h2>Written and medically reviewed by ' . esc_html($profile['name']) . '</h2>'
        . '<p>This article reflects Chris\'s real clinical experience treating common urgent-care conditions through NPCWoods Telemedicine. Content is reviewed for accuracy, updated over time, and paired with clear guidance on when text-based care is appropriate and when in-person care matters more.</p>'
        . '</div>'
        . '<div class="npc-post-trust-grid">'
        . '<div class="npc-post-trust-card"><div class="npc-post-trust-label">Credentials</div><p>' . esc_html($profile['title']) . '. Licensed in ' . esc_html($profile['states']) . '. NPI ' . esc_html($profile['npi']) . '.</p></div>'
        . '<div class="npc-post-trust-card"><div class="npc-post-trust-label">Review Dates</div><p>Published ' . esc_html($published) . '. Last reviewed and updated ' . esc_html($updated) . '.</p></div>'
        . '<div class="npc-post-trust-card"><div class="npc-post-trust-label">Care Model</div><p>You text Chris directly. No AI triage, no call center, and no copy-paste handoff between strangers.</p></div>'
        . '<div class="npc-post-trust-card"><div class="npc-post-trust-label">Safety Note</div><p>This article is educational only. For chest pain, trouble breathing, severe dehydration, confusion, or other emergencies, call 911 or seek urgent in-person care.</p></div>'
        . '</div>'
        . '<div class="npc-post-trust-links">'
        . '<a href="' . esc_url($profile['about_url']) . '">About Chris</a>'
        . '<a class="npc-post-trust-secondary" href="' . esc_url($profile['npi_url']) . '" target="_blank" rel="noopener">Verify NPI</a>'
        . '<a class="npc-post-trust-secondary" href="' . esc_url($profile['disclaimer_url']) . '">Medical disclaimer</a>'
        . '</div>'
        . $related_markup
        . '</section>';

    return $trust . $content;
}, 20);
