import json
import subprocess
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAY_PAGE = REPO_ROOT / "landing-pages" / "pay" / "index.html"


class PayAttributionTest(unittest.TestCase):
    def test_google_click_params_create_parseable_stripe_reference(self):
        redirect = run_pay_submit("?utm_source=google&utm_medium=cpc&utm_campaign=mesa-test&gclid=TESTGCLID")
        params = redirect["params"]

        self.assertEqual("google", params["utm_source"])
        self.assertEqual("cpc", params["utm_medium"])
        self.assertEqual("mesa-test", params["utm_campaign"])
        self.assertEqual("TESTGCLID", params["gclid"])
        self.assertEqual("google-cpc-mesa-test-gclid-TESTGCLID", params["client_reference_id"])

    def test_stored_landing_page_attribution_survives_plain_pay_visit(self):
        stored_touch = {
            "source": "google",
            "medium": "cpc",
            "campaign": "stored-campaign",
            "click_id": "STOREDGCLID",
            "click_id_type": "gclid",
            "expiresAt": 4102444800000,
        }

        redirect = run_pay_submit("", stored_touch)
        params = redirect["params"]

        self.assertEqual("google", params["utm_source"])
        self.assertEqual("cpc", params["utm_medium"])
        self.assertEqual("stored-campaign", params["utm_campaign"])
        self.assertEqual("STOREDGCLID", params["gclid"])
        self.assertEqual("google-cpc-stored-campaign-gclid-STOREDGCLID", params["client_reference_id"])

    def test_plain_pay_still_defaults_to_manual_spruce_reference(self):
        redirect = run_pay_submit("")
        params = redirect["params"]

        self.assertEqual("spruce", params["utm_source"])
        self.assertEqual("text", params["utm_medium"])
        self.assertEqual("manual-payment", params["utm_campaign"])
        self.assertEqual("spruce-manual-payment", params["client_reference_id"])

    def test_optional_heard_source_tags_plain_referral_payment(self):
        redirect = run_pay_submit("", heard_source="friend_family")
        params = redirect["params"]

        self.assertEqual("referral", params["utm_source"])
        self.assertEqual("wordofmouth", params["utm_medium"])
        self.assertEqual("heard-friend-family", params["utm_campaign"])
        self.assertEqual("referral-wordofmouth-heard-friend-family", params["client_reference_id"])

    def test_optional_heard_source_does_not_override_google_click_params(self):
        redirect = run_pay_submit(
            "?utm_source=google&utm_medium=cpc&utm_campaign=mesa-test&gclid=TESTGCLID",
            heard_source="friend_family",
        )
        params = redirect["params"]

        self.assertEqual("google", params["utm_source"])
        self.assertEqual("cpc", params["utm_medium"])
        self.assertEqual("mesa-test", params["utm_campaign"])
        self.assertEqual("TESTGCLID", params["gclid"])
        self.assertEqual("google-cpc-mesa-test-gclid-TESTGCLID", params["client_reference_id"])


def run_pay_submit(query: str, stored_touch: dict | None = None, heard_source: str = "") -> dict:
    runner = textwrap.dedent(
        """
        const fs = require('fs');
        const pagePath = process.argv[1];
        const query = process.argv[2] || '';
        const storedTouch = process.argv[3] ? JSON.parse(process.argv[3]) : null;
        const heardSource = process.argv[4] || '';
        const html = fs.readFileSync(pagePath, 'utf8');
        const match = html.match(/<script>\\s*(\\(function\\(\\) \\{[\\s\\S]*?\\}\\)\\(\\);)\\s*<\\/script>\\s*<\\/body>/);
        if (!match) throw new Error('pay submit script not found');

        const listeners = {};
        function makeElement(id, initial = {}) {
          const attrs = new Set(initial.attrs || []);
          return {
            id,
            value: initial.value || '',
            checked: !!initial.checked,
            classList: { add() {}, remove() {} },
            addEventListener(type, fn) { listeners[id + ':' + type] = fn; },
            removeAttribute(name) { attrs.delete(name); },
            setAttribute(name) { attrs.add(name); },
            hasAttribute(name) { return attrs.has(name); },
          };
        }
        function makeChip(source) {
          return {
            dataset: { source },
            classList: { add() {}, remove() {}, toggle() {} },
            setAttribute() {},
            getBoundingClientRect() { return { left: 100, top: 100, width: 80, height: 32 }; },
            addEventListener(type, fn) { listeners['heardChip:' + source + ':' + type] = fn; },
          };
        }

        const elements = {
          attestationForm: makeElement('attestationForm'),
          stateSelect: makeElement('stateSelect'),
          chkLocation: makeElement('chkLocation', { attrs: ['disabled'] }),
          chkFee: makeElement('chkFee'),
          chkTerms: makeElement('chkTerms'),
          heardSelect: makeElement('heardSelect'),
          btnSubmit: makeElement('btnSubmit', { attrs: ['disabled'] }),
        };
        const heardChips = [
          makeChip('google_search'),
          makeChip('friend_family'),
          makeChip('facebook_instagram'),
          makeChip('returning_visitor'),
          makeChip('other'),
        ];
        let redirected = '';
        const storage = {};
        if (storedTouch) {
          storage.npc_attribution_last = JSON.stringify(storedTouch);
        }

        global.document = {
          getElementById(id) { return elements[id]; },
          querySelectorAll(selector) { return selector === '.source-chip' ? heardChips : []; },
          createElement() {
            return {
              style: { setProperty() {} },
              className: '',
              addEventListener(_type, fn) { fn(); },
              remove() {},
            };
          },
          body: { appendChild() {} },
        };
        global.window = {
          location: {
            search: query,
            replace(url) { redirected = url; },
          },
          sessionStorage: { setItem(key, value) { storage[key] = String(value); } },
          localStorage: { getItem(key) { return storage[key] || null; } },
        };
        global.URL = URL;
        global.URLSearchParams = URLSearchParams;

        eval(match[1]);
        if (heardSource) {
          const chipListener = listeners['heardChip:' + heardSource + ':click'];
          if (chipListener) chipListener({ preventDefault() {} });
        }
        elements.stateSelect.value = 'AZ';
        listeners['stateSelect:change']();
        elements.chkLocation.checked = true;
        elements.chkFee.checked = true;
        elements.chkTerms.checked = true;
        listeners['chkLocation:change']();
        listeners['chkFee:change']();
        listeners['chkTerms:change']();
        listeners['attestationForm:submit']({ preventDefault() {} });

        const finalUrl = new URL(redirected);
        const params = {};
        for (const [key, value] of finalUrl.searchParams.entries()) {
          params[key] = value;
        }
        console.log(JSON.stringify({ url: redirected, params }));
        """
    )
    completed = subprocess.run(
        ["node", "-e", runner, str(PAY_PAGE), query, json.dumps(stored_touch) if stored_touch else "", heard_source],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


if __name__ == "__main__":
    unittest.main()
