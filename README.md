# Liberty Lend SA - website preview

A responsive, dependency-free, static website for a South African small-personal-loan campaign, currently in **preview-only** mode. The brand is separate from Thynkverse. All website code lives in this repository.

## What is built

- Responsive campaign landing page, custom SVG visual identity, mobile navigation.
- Working local planning tool that accepts a **purpose and a customer-entered amount only**. It does **not** calculate borrowing costs, request contact/ID/bank data, save inputs, contact an API, run credit checks or apply for credit.
- Explanation of the intended responsible lending process, five FAQ entries, privacy notice and website terms.
- Accessible labels, keyboard operation, skip link, reduced-motion support, responsive breakpoints and semantic HTML.
- No framework, analytics, tracking pixels, paid services or build step.
- SEO metadata, share artwork and preview-only noindex / robots.txt.
- Optional Vercel security headers in `vercel.json`.

## Project files

```text
index.html                  Homepage and planning tool
styles.css                  Design tokens, layout and responsive styles
script.js                   Mobile menu and local planning interaction
privacy.html                Preview privacy notice
terms.html                  Preview website terms
assets/favicon.svg          Original Liberty Lend SA concept icon
assets/social-preview.svg   Original social preview artwork
robots.txt                  Prevents indexing in preview
vercel.json                 Optional static hosting and security headers
README.md                   Setup, release checklist and design notes
tests/test_structure.py     No-dependency structural checks
tests/test_site.py          Optional Playwright visual and interaction checks
```

## Run locally

No package install required:

```bash
python3 -m http.server 5173
```

Open <http://localhost:5173>. Alternatively, open `index.html` directly in your browser.

## Deploy to Vercel

1. Import this GitHub repository in Vercel.
2. Choose **Other** as the framework preset; no build command or output directory is needed.
3. Use a **private/protected preview deployment** while lender status and copy await verification.
4. Do **not** enable a public credit campaign until the release checklist below has passed.

Pushing to GitHub is not the same as deploying the website. The website may also be hosted on any static hosting provider.

## Required before opening a real lending campaign

The owner / appropriately qualified advisers must check and approve at least:

- [ ] Registered operator's correct legal name and company registration details.
- [ ] Lending arrangement: whether Liberty Lend SA is the registered credit provider, an authorised intermediary, or purely a marketing brand. Verify the provider's **NCR registration and role** before advertising credit.
- [ ] Properly substantiated loan products, eligibility rules, rate structure, repayment terms, initiation and service fees and compulsory insurance (if any).
- [ ] South African National Credit Act advertising review, including required disclosures when an interest rate, monthly repayment or loan cost is advertised. Avoid prohibited promises and misleading claims.
- [ ] Approved credit assessment and pre-agreement quotation processes, including affordability assessment and adverse-outcome procedures.
- [ ] Real verified contact details, customer service and complaints channels, physical address, legal terms and disclosures.
- [ ] POPIA-compliant privacy policy, Information Officer details, processors, purposes, legal basis, security, retention and data subject process.
- [ ] A security-reviewed application backend/CRM integration before collecting personal or financial information. Never commit tokens or API keys to a public repository.
- [ ] Independent legal/compliance signoff on public copy and deployment.
- [ ] Remove `noindex,nofollow` and `robots.txt` blocking only after approval; update share metadata with the real domain and retest.

**Important**: Avoid replacing the planning tool with a cost calculator until the actual interest, fees, insurance, number of instalments, total repayment and applicable terms can be disclosed accurately. Loan cost advertising has specific content requirements.

Useful references:

- [National Credit Act, section 40 - registration](https://api.acts.co.za/national-credit-act-2005/40__registration_of_credit_providers.php)
- [National Credit Act, section 76 - credit advertising](https://api.acts.co.za/national-credit-act-2005/76__advertising_practices.php)
- [National Credit Regulations, regulation 21 - advertising content](https://api.acts.co.za/national-credit-act-2005/r489_21__required_content_for_advertising_practices.php)
- [Information Regulator South Africa](https://inforegulator.org.za/)

## Design direction

**Clear headspace**: approachable, direct, confident. Deep teal (`#123A49`) anchors trust; fresh green (`#1C8B79`), mint (`#DDF1E5`) and pale citrus (`#E7F3B1`) support warm, measured optimism. An open arch illustrates making room for life's next step. Original vector assets are included and can be replaced if the client already has an approved logo. No Thynkverse client branding is used.

## Implementation notes

- The site assumes **no** user account, backend, database, payment gateway, WhatsApp account, email service or lending partner. These are not silently faked.
- Privacy and website terms are **preview disclosures**, not a final legal privacy policy or an agreed loan contract.
- The preview banner, noindex rule, and disabled applications are intentional; do not remove them without approval.
- Screens and customer data used for testing must remain synthetic.

## Checks

Run `python3 tests/test_structure.py` for dependency-free source tests. With Playwright and its Chromium browser installed, run `python3 tests/test_site.py` to exercise mobile navigation, the planning tool, FAQ, page loading and capture responsive screenshots. This second test requires a browser environment permitting access to local files.
