# Doctor/insurance scrub: WordPress-database pages (not deployable via deploy.py)
v2 after Chris kept legal/citation physician wording. Exact find -> replace, per post (WP ID). Meaning and medical claims unchanged.

## is-text-based-telehealth-safe (post 439)
- "For physicians, check the state medical board." -> "For other clinicians, check the state medical board."
## cash-pay-telehealth-reasons (post 524)
- "No insurance navigating, no networks, no denied claims." -> "No plan paperwork, no networks, no denied claims."
## telehealth-vs-urgent-care-cost-speed (post 305)
- "Cost with insurance:" -> "Cost with a health plan:"
- "Cost without insurance:" -> "Self-pay cost:"
- "No insurance needed, no copay" -> "Self-pay, no copay"
- "(or $200+ without insurance)" -> "(or $200+ self-pay)"
- "No app, no account, no insurance needed." -> "No app, no account. Self-pay."
## terms-of-service (page 317), legal text
- "We do not bill insurance." -> "We do not bill third-party payers; every visit is self-pay."

Applied live 2026-10-10 ~7:23 AM ET via WP REST (deploy.py load_env auth). Post 469 intentionally unchanged (Chris kept legal/scope-of-practice wording and the quote). Originals: content-output/deploy-backups/2026-10-10/wp-content/*.json
