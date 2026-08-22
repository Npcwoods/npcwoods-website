<?php
/**
 * Plugin Name: NPCWoods Hide Floating Contact Strip
 * Description: Suppresses the fixed body::after teal phone/fax bar site-wide (owner request, 2026-06-25).
 *              The strip is defined in the Customizer "Additional CSS" (FLOATING CONTACT STRIP block).
 *              This prints a late, higher-priority override so the bar is hidden on every page. The
 *              clean long-term fix is to delete that block from Appearance > Customize > Additional CSS.
 * Version: 1.0
 */

if (!defined('ABSPATH')) { exit; }

// Print after the Customizer custom CSS (wp_head priority 101) so this override wins.
add_action('wp_head', function () {
    echo "\n<style id=\"npcwoods-hide-contact-strip\">body::after{content:none !important;display:none !important;}</style>\n";
}, 1000);
