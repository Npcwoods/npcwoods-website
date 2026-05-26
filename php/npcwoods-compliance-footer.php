<?php
/**
 * Plugin Name: NPCWoods Compliance Footer
 * Description: Adds LegitScript-compliant footer with legal links, credentials, and disclaimers
 * Version: 1.1
 * Author: ChrisOS
 */

// Inject compliance footer on all pages
add_action('wp_footer', 'npcwoods_compliance_footer', 99);

function npcwoods_compliance_footer() {
    if (!empty($GLOBALS['npcwoods_shared_footer_rendered'])) {
        return;
    }
    ?>
    <style>
        .npcwoods-compliance-footer {
            background-color: #1a1a2e;
            color: #cccccc;
            padding: 40px 20px 20px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            border-top: 3px solid #2563eb;
        }
        .npcwoods-compliance-footer .footer-inner {
            max-width: 1000px;
            margin: 0 auto;
        }
        .npcwoods-compliance-footer .footer-business {
            text-align: center;
            margin-bottom: 20px;
        }
        .npcwoods-compliance-footer .footer-business-name {
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 4px;
        }
        .npcwoods-compliance-footer .footer-credentials {
            color: #aaaaaa;
            font-size: 13px;
        }
        .npcwoods-compliance-footer .footer-contact {
            text-align: center;
            margin-bottom: 20px;
            color: #aaaaaa;
            font-size: 13px;
        }
        .npcwoods-compliance-footer .footer-contact a {
            color: #60a5fa;
            text-decoration: none;
        }
        .npcwoods-compliance-footer .footer-contact a:hover {
            text-decoration: underline;
        }
        .npcwoods-compliance-footer .footer-legal-links {
            text-align: center;
            margin-bottom: 20px;
            padding: 15px 0;
            border-top: 1px solid #333;
            border-bottom: 1px solid #333;
        }
        .npcwoods-compliance-footer .footer-legal-links a {
            color: #60a5fa;
            text-decoration: none;
            margin: 0 12px;
            font-size: 13px;
        }
        .npcwoods-compliance-footer .footer-legal-links a:hover {
            text-decoration: underline;
        }
        .npcwoods-compliance-footer .footer-disclaimer {
            text-align: center;
            font-size: 12px;
            color: #888888;
            max-width: 700px;
            margin: 0 auto 15px;
            line-height: 1.5;
        }
        .npcwoods-compliance-footer .footer-disclaimer strong {
            color: #ff6b6b;
        }
        .npcwoods-compliance-footer .footer-legitscript {
            text-align: center;
            margin-bottom: 15px;
        }
        .npcwoods-compliance-footer .footer-copyright {
            text-align: center;
            font-size: 12px;
            color: #666666;
        }
        .npcwoods-compliance-footer .hipaa-badge {
            display: inline-block;
            background: #1e3a5f;
            color: #60a5fa;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="npcwoods-compliance-footer">
        <div class="footer-inner">
            <div class="footer-business">
                <div class="footer-business-name">NPCWoods Telemedicine, PLLC</div>
                <div class="footer-credentials">
                    Chris Woods, MSN, FNP-C &nbsp;|&nbsp; NPI: 1285125468<br>
                    AZ: 320600 | CO: C-APN.0103723-C-NP | GA: APRN-NP319386 | ID: 1671854 | IA: A183070 | MT: APRN-260601 | NV: 886822 | NM: 82936 | NC: 5010551 | OR: 10043494 | UT: 14202514-4405
                </div>
            </div>

            <div class="footer-contact">
                <a href="tel:4806394722">(480) 639-4722</a> &nbsp;|&nbsp;
                <a href="mailto:cwoods@npcwoods.com">cwoods@npcwoods.com</a><br>
                Telehealth service &middot; Licensed in AZ, CO, GA, ID, IA, MT, NV, NM, NC, OR, UT
            </div>

            <div class="footer-legal-links">
                <a href="/privacy-policy/">Privacy Policy</a>
                <a href="/terms-of-service/">Terms of Service</a>
                <a href="/medical-disclaimer/">Medical Disclaimer</a>
            </div>

            <div class="footer-disclaimer">
                <strong>This site does not provide emergency medical services.</strong>
                If you are experiencing a medical emergency, call 911 immediately.
                Telehealth services are not a substitute for in-person medical care when clinically indicated.
                Individual results may vary.
            </div>

            <div class="footer-legitscript">
                <a href="https://www.legitscript.com/websites/?checker_keywords=npcwoods.com" target="_blank" title="Verify LegitScript Approval for www.npcwoods.com">
                    <img src="https://static.legitscript.com/seals/45807860.png" alt="Verify Approval for www.npcwoods.com" width="73" height="79" />
                </a>
            </div>

            <div class="footer-copyright">
                &copy; <?php echo date('Y'); ?> NPCWoods Telemedicine, PLLC. All rights reserved.
                &nbsp;|&nbsp; <span class="hipaa-badge">HIPAA COMPLIANT</span>
            </div>
        </div>
    </div>
    <?php
}
