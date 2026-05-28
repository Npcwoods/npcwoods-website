from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


class NoPhiAnalyticsPayloadsTest(unittest.TestCase):
    def test_tracking_js_does_not_send_full_sms_href_to_analytics(self):
        for rel_path in ("html/tracking.js", "html/shared/tracking.js"):
            text = read(rel_path)

            self.assertNotIn("event_label: target.getAttribute('href')", text)
            self.assertIn("event_label: safeInteractionLabel(target)", text)

    def test_trust_video_quiz_does_not_send_symptom_or_duration_values(self):
        text = read("landing-pages/trust-video/index.html")

        self.assertNotIn("gtag('event', 'quiz_symptom', { symptom:", text)
        self.assertNotIn("gtag('event', 'quiz_complete', { symptom:", text)
        self.assertIn("gtag('event', 'quiz_symptom', { event_category:", text)
        self.assertIn("gtag('event', 'quiz_complete', { event_category:", text)

    def test_thank_you_scrubs_checkout_id_before_pixels_load(self):
        text = read("html/thank-you/index.html")
        scrub_marker = "window.NPC_CHECKOUT_IDENTIFIER"
        analytics_marker = "https://www.googletagmanager.com/gtm.js"

        self.assertIn(scrub_marker, text)
        self.assertLess(text.index(scrub_marker), text.index(analytics_marker))
        self.assertIn(
            "history.replaceState(null, document.title, window.location.pathname);",
            text,
        )

    def test_thank_you_does_not_send_raw_checkout_id_to_meta_or_ga(self):
        text = read("html/thank-you/index.html")

        self.assertNotIn("transaction_id: transactionId", text)
        self.assertNotIn("order_id: eventPayload.transaction_id", text)
        self.assertNotIn("'cd[order_id]': eventPayload.transaction_id", text)
        self.assertIn("hashCheckoutIdentifier(transactionId)", text)
        self.assertIn("dl: sanitizedPageUrl", text)


if __name__ == "__main__":
    unittest.main()
