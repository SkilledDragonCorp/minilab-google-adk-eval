# Security Policy

This is a **SkilledDragon educational minilab**, not a production product. It is published so people can try a small, keyed-off demo. We do **not** maintain these repos on a regular schedule and we do **not** operate a vulnerability response program for them.

## Contact

General questions: **hello@skilleddragon.com**  
Do not use a dedicated security mailbox for this repo — none exists.

## If you find an issue

- Prefer reporting **upstream** when the issue is in [google/adk-python](https://github.com/google/adk-python) or other dependencies.
- For something specific to this minilab’s wrapper scripts, you may email hello@skilleddragon.com. There is **no SLA**, and we may not patch or reply quickly.
- Do not expect private coordinated disclosure or paid bounty handling here.

## Minilab hygiene

- Secrets only via environment variables; never commit `.env`.
- CI runs **gitleaks** and **pip-audit** when configured.
- Keyless eval path must skip cleanly without `GOOGLE_API_KEY`.

Use at your own risk. Pin versions, review the code, and treat this as sample material.
