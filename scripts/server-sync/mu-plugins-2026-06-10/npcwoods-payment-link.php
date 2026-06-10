<?php
/**
 * Plugin Name: NPCWoods Payment Link
 * Description: Serves /pay/ as a noindex browser redirect to Stripe with safe attribution labels.
 */

add_action( 'template_redirect', function() {
    if ( ! is_page() ) {
        return;
    }

    $slug = get_post_field( 'post_name', get_queried_object_id() );
    if ( 'pay' !== $slug ) {
        return;
    }

    nocache_headers();
    header( 'Content-Type: text/html; charset=UTF-8', true );
    header( 'X-Robots-Tag: noindex, nofollow', true );
    header( 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0', true );
    header( 'Surrogate-Control: no-store', true );
    header( 'Pragma: no-cache', true );
    ?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>Redirecting to secure payment | NPCWoods</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172033;
      background: #f7faf8;
    }
    main {
      width: min(520px, calc(100% - 32px));
      text-align: center;
    }
    a { color: #0f766e; font-weight: 700; }
  </style>
</head>
<body>
  <main>
    <p>Redirecting to secure payment...</p>
    <p><a id="pay-fallback" href="https://buy.stripe.com/8x2eVcevF2M4cWzcf2dQQ03?utm_source=spruce&utm_medium=text&utm_campaign=manual-payment&client_reference_id=spruce-manual-payment">Continue to payment</a></p>
  </main>
  <script>
  (function() {
    const stripeUrl = new URL('https://buy.stripe.com/8x2eVcevF2M4cWzcf2dQQ03');
    const sourceParams = new URLSearchParams(window.location.search);
    const aliases = {
      client_reference_id: ['client_reference_id', 'ref'],
      utm_source: ['utm_source', 'source', 'src'],
      utm_medium: ['utm_medium', 'medium'],
      utm_campaign: ['utm_campaign', 'campaign', 'cmp'],
      utm_content: ['utm_content', 'content', 'ad'],
      utm_term: ['utm_term', 'term']
    };
    const defaults = {
      utm_source: 'spruce',
      utm_medium: 'text',
      utm_campaign: 'manual-payment'
    };

    function clean(value) {
      return String(value || '')
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9_.-]+/g, '-')
        .replace(/^[-_.]+|[-_.]+$/g, '')
        .slice(0, 80);
    }

    function firstClean(keys) {
      for (const key of keys) {
        if (!sourceParams.has(key)) continue;
        const value = clean(sourceParams.get(key));
        if (value) return value;
      }
      return '';
    }

    const output = new URLSearchParams(defaults);
    let explicitReference = false;
    for (const [target, keys] of Object.entries(aliases)) {
      const value = firstClean(keys);
      if (!value) continue;
      output.set(target, value);
      if (target === 'client_reference_id') explicitReference = true;
    }

    if (!explicitReference) {
      const source = output.get('utm_source') || 'unknown';
      const medium = output.get('utm_medium') || 'unknown';
      const campaign = output.get('utm_campaign') || 'payment';
      if (source === 'spruce' && medium === 'text' && campaign === 'manual-payment') {
        output.set('client_reference_id', 'spruce-manual-payment');
      } else {
        output.set('client_reference_id', clean([source, medium, campaign].join('-')) || 'npcwoods-payment');
      }
    }

    stripeUrl.search = output.toString();
    document.getElementById('pay-fallback').href = stripeUrl.toString();
    window.location.replace(stripeUrl.toString());
  })();
  </script>
</body>
</html>
    <?php
    exit;
}, 1 );
