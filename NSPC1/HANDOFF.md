# Shared Kitchen Landing Page — Handoff / Spec

**Client:** North Shore Presbyterian Church (NSPC), Shorewood WI
**Page:** the "Shared Kitchen" ministry landing page
**Live target:** `https://www.northshorepres.org/shared-kitchen` (Squarespace)
**Status:** built, reviewed through Rodger (RJ) 7.10.26 round. The live page was verified current on 2026-10-13 — its `<style>` block and body markup matched this build exactly. Seven `!important` colour overrides have been added since (§6), so one more re-paste is owed.

> This doc is the single source of truth for continuing the page in VS Code / Claude Code. Everything here is NSPC only.

---

## 1. What this is

A single, self-contained HTML landing page for NSPC's Shared Kitchen ministry — a renovated commercial kitchen used as a community hub and event venue, with a fundraising ask. The page is designed to live **inside the existing Squarespace site** (nested under the site's own global header/nav and footer), not as a standalone site.

There are two shipping forms of the exact same page:

| File | What it is | Use |
|---|---|---|
| `index.html` (this repo) | References images from `images/`; carries a Pages-only `noindex` | GitHub Pages hosting, local editing |
| `shared_kitchen_page.html` (standalone) | Same markup, **images inlined as base64**, `noindex` stripped | Paste into a Squarespace **Code Block** |

When you change `index.html`, regenerate the standalone with `python build-standalone.py` (see §7).
Never hand-edit `shared_kitchen_page.html` — it is generated.

**The `noindex` line.** `index.html` carries `<meta name="robots" content="noindex,nofollow"><!-- PAGES-ONLY -->`
so the GitHub Pages copy cannot compete in search with the real page at
`northshorepres.org/shared-kitchen`. `build-standalone.py` strips that line, so it never
reaches Squarespace. If you move the meta tag, keep the `<!-- PAGES-ONLY -->` marker on it —
the build fails loudly if it cannot find exactly one.

---

## 2. How to run / preview

It's a static page — no build step.

```bash
# from this folder
python3 -m http.server 8000
# open http://localhost:8000
```

It is also published, for review, at **https://dk1541.github.io/NSPC/NSPC1/** — a copy of the
live page, not the live page itself. The church's own site refresh previews live one level up at
https://dk1541.github.io/NSPC/ and are an unrelated piece of work in a different design system.

Edit `index.html` directly. Everything (CSS + one small JS snippet) is inline in that one file.

---

## 3. Deploy (Squarespace)

1. Open `shared_kitchen_page.html`, copy **all** of it.
2. In Squarespace, edit the `/shared-kitchen` page → the **Code Block** → paste over the old code.
3. **Save + Publish.**

The page is built to nest inside Squarespace: it has **no header of its own** (removed so there's no duplicate logo / nav), and the site's global header + footer wrap around it automatically.

> ⚠️ **The most important constraint — read §6 before touching colors or fonts.**

---

## 4. File structure

```
shared-kitchen-site/
├── index.html              # the page (CSS + JS inline)
├── build-standalone.py     # regenerates the Squarespace paste file
├── shared_kitchen_page.html  # GENERATED — do not hand-edit
├── images/
│   ├── nspc-logo.png       # pineapple logo (footer)
│   ├── hero.jpg            # hero bg — hands kneading bread dough
│   ├── kitchen-bake.jpg    # photo strip — two bakers
│   ├── kitchen-team.jpg    # photo strip — two cooks
│   ├── kitchen-pots.jpg    # photo strip — pots simmering
│   ├── congregation.jpg    # community — REAL NSPC congregation photo
│   └── handshake.jpg       # community — REAL NSPC handshake photo
├── README.md
└── HANDOFF.md              # this file
```

Related loose files that ship alongside (not in this repo, in the outputs folder):
`shared_kitchen_page.html` (standalone), `shared-kitchen-qr.png` / `.svg` / `-plain.png` (QR to the live page, navy + optional pineapple).

---

## 5. Brand system

Pulled from the official **Shared Kitchen deck** (`SharedKitchenDeck_BIZ`).

**Colors** (CSS custom properties on `:root`):

| Token | Hex | Use |
|---|---|---|
| `--navy` / `--text-heading` / `--bg-dark` | `#1C3F6E` | headings, dark bands |
| `--coral` | `#E1793A` | primary accent, buttons, pillar 1 |
| `--teal` | `#4EA58D` | pillar 2, "Making Our Mission" headline |
| `--blue` | `#3E93CE` | pillar 3 |
| `--gold` / `--accent` | `#CB9A45` | rules, quote "+", separators |
| `--bg-page` | `#FBFAF7` | page background (warm off-white) |
| `--bg-alt` / `--card` | `#FFFFFF` | cards, alternating sections |
| `--text-body` | `#374049` | body copy |
| `--text-on-dark` | `#F4F2EA` | text on navy |
| `--heading-on-dark` | `#ECD79E` | gold-cream accent on navy |

**Fonts** (Google Fonts): **Poppins** (headings, buttons, eyebrows, UI) + **Mulish** (body). Body weight is **500** (deliberately heavier so it isn't faint on mobile).

**Logo:** the NSPC pineapple (`images/nspc-logo.png`).

**Hero motif:** three overlapping outlined circles (coral / white / teal) with a centered white **"+" cross** — echoes the deck's "overlapping circles + plus" graphic. The cross is a standalone `.hero-plus` element (NOT inside the `.circles` group, which is at 50% opacity — keeping the cross separate is what makes it bright and centered).

**Color scheme:** **LIGHT only, on every device.** There is intentionally no dark-mode CSS. See §6.

---

## 6. ⚠️ Critical constraint — Squarespace theme override

The single biggest source of bugs on this page: **Squarespace's theme (especially its dark-mode treatment) tries to override the page's fonts and colors**, which made the headline go black and the font change between light/dark mode on mobile.

**The fix is already in place and must be preserved:**

- A block of `!important` overrides at the **end of the `<style>`** re-asserts every brand color AND `font-family` so the host theme can't repaint or re-font them. (Search the file for `Re-assert brand colors`.)
- Fonts are loaded **twice** — a `<link>` tag *and* an `@import` inside the `<style>` — so they still load if Squarespace strips one.
- `color-scheme: light` is set and there is **no `prefers-color-scheme: dark` block at all**, so the page looks identical on phone, tablet, laptop, desktop, in light or dark mode.
- `-webkit-font-smoothing:antialiased` keeps light text crisp on the dark bands.

**If you add any new colored text or heading, add a matching `!important` line to that override block**, or Squarespace may recolor/re-font it in dark mode. Always test the *published* Squarespace page in phone dark mode, not just local preview (local has no host theme).

**Audited 2026-10-13.** Sixteen of the page's twenty-three coloured selectors had a colour
override; seven did not. All seven now do. The two that mattered were light text sitting on the
navy bands — `.cta h2 span` (the gold-cream "make a difference.") and `.socials a` — either of
which would have gone dark-on-dark and vanished. `.venue h2 span` had its line but its twin
`.cta h2 span` did not, which is exactly how this bug recurs: a selector gets copied, its
override does not. To re-run the audit, compare the selectors carrying `color:` in the main
stylesheet against those carrying `color:` in the override block; a `font-family` line for a
selector does **not** protect its colour.

---

## 7. Regenerate the standalone (base64) file after edits

The Squarespace file must have images inlined. After editing `index.html`:

```bash
python build-standalone.py
```

It walks `images/` rather than a hard-coded list, so a new photograph needs no change here, and
it refuses to write the file if an image reference survives or if the `PAGES-ONLY` line is
missing. Then paste `shared_kitchen_page.html` into the Squarespace Code Block (§3).

---

## 8. Section map (top → bottom)

| # | Section (`class`) | Content |
|---|---|---|
| 1 | **Hero** `.hero` | Eyebrow "North Shore Presbyterian Church · Shared Kitchen"; H1 **"Multiplying Our Mission"**; sub "Our Shared Kitchen builds on our long-standing food ministry — nourishing **mind, body, and spirit** across the North Shore." Circles + "+" motif over `hero.jpg`. **No button** (moved to §6 giving section per RJ 7.10). |
| 2 | **Venue band** `.venue` | "The Perfect Venue for **Your Next Event**" + 4 icons: Fundraisers · Family Reunions · Baby Showers · Community Outreach. |
| 3 | **Intro** `.intro` | Eyebrow "Multiplying Our Mission"; two-tier headline **"More than a kitchen." / "A gathering place."**; Loaves-and-Fishes paragraph; gold rule. |
| 4 | **Pillars** `.pillars` | 3 cards: **Building on Our Legacy** (coral) · **Being Good Stewards** (teal) · **Enlivens the Building** (blue). |
| 5 | **Photo strip** `.strip` | "**Life in the Shared Kitchen**" + 3 photos (bake / team / pots). |
| 6 | **Making Our Mission Possible** `.give` | Fundraising ask (RJ's copy verbatim), teal headline, **"Contribute Today"** button → Vanco campaign. The page's **only** contribution button. |
| 7 | **Quote** `.quote` | "It is always a good day to be a neighbor." |
| 8 | **Community** `.community` | "**A Place for Community**"; two REAL NSPC photos (congregation "Gathered as neighbors" left / handshake "Stronger together" right); tick list; **"Learn About Us"** outline button → church homepage. |
| 9 | **CTA** `.cta` | "Together, we can **make a difference.**" + social links (Instagram / Facebook / YouTube). |
| 10 | **Footer** `.foot` | Pineapple logo, tagline, address, phone, email, mind/body/spirit motto. |

---

## 9. Link & contact inventory

**Buttons / links:**
- Contribute Today (§6) → `https://secure.myvanco.com/L-ZMZZ/campaign/C-16EHE` (Shared Kitchen Vanco campaign)
- Learn About Us (§8) → `https://www.northshorepres.org`
- Instagram → `https://www.instagram.com/northshorepres?igsh=MWhyZzFsMjY5YXhpYQ==`
- Facebook → `https://www.facebook.com/share/196nEEHWTy/?mibextid=wwXIfr`
- YouTube → `https://youtube.com/@northshorepresbyterianchur3484?si=sMjTiiy8PhioCkVf`

**Footer contact (do not change without confirming):**
- North Shore Presbyterian Church · 4048 North Bartlett Avenue · Shorewood, WI 53211
- Phone `414-332-8130` (`tel:+14143328130`) · Email `office@northshorepres.org`

**Vanco note:** the Shared Kitchen *campaign* page is `…/campaign/C-16EHE`. The general giving home is `…/L-ZMZZ/home`. The page currently points all giving at the Shared Kitchen campaign.

---

## 10. Change history (what's been decided — don't undo these)

Git log, newest first, with the reasoning:

1. **Making Our Mission Possible section added** (RJ 7.10.26) — new giving section placed *after* "Life in the Shared Kitchen" so people learn what they're funding first; contribution button moved out of the hero. Now **one** Contribute button total.
2. **Fonts locked** with `!important` + `@import` + font-smoothing — fixed font changing between light/dark on mobile (Squarespace was overriding).
3. **Mobile polish** — body text set to Mulish 500 (heavier/darker) so it's not faint; "+" cross moved out of the faded circle group so it's centered and visible.
4. **Removed bottom Contribute button** (earlier state) — then superseded by #1 which made the give-section button the single CTA.
5. **Community photos** — real NSPC congregation photo (left) + handshake under "Stronger together"; dropped the stock "joined hands" image.
6. **Rodger's 7.8 feedback** — headline → "Multiplying Our Mission" and forced white vs host CSS; centered hero circles; "community kitchen" → "**Shared Kitchen**" everywhere (capital S/K is house style); hero button → Contribute (SK campaign); added "Learn About Us" in community section.
7. **Removed internal header** — so the page nests under the Squarespace site nav (no duplicate logo/button).
8. **Two-tier intro headline** — fixed an orphaned em-dash wrap; now "More than a kitchen." / "A gathering place."
9. **Wired buttons** to Vanco + homepage.
10. **Rebranded to the Shared Kitchen deck** — Poppins/Mulish, navy/coral/teal/gold, pineapple logo, circles motif, approved photos, fixed social links.
11. **Fixed invisible content** — reveal animations are JS-gated; added the `.js` class + IntersectionObserver so content shows even if JS is slow.

**House style rules to honor:**
- Always "**Shared Kitchen**" (capital S, K). Never "community kitchen."
- Fundraising ask comes **after** the Shared Kitchen explanation, not before (RJ's strategy).
- No kids' faces on any NSPC collateral unless photo permission is confirmed.

---

## 11. Open / pending items

- [x] ~~Re-paste + republish the latest build~~ — done before 2026-10-13. Verified by fetching the
      live page: its `<style>` block and full body markup matched this build byte for byte.
- [ ] **Re-paste + republish again** to pick up the seven colour overrides added in §6. The diff
      against the previously published file is exactly those seven lines and nothing else.
- [ ] After republishing, **test the live page in phone dark mode** (local preview can't catch the
      Squarespace theme override). The two to look at are the gold-cream "make a difference." in
      the CTA band and the social links beneath it.
- [ ] Decide whether the footer should be trimmed if the Squarespace global footer already repeats the church's contact info (would otherwise show twice).
- [ ] Optional: a QR code to `/shared-kitchen` already exists (`shared-kitchen-qr.*`) if it's wanted on any printed piece.
- [ ] Confirm giving should stay 100% on the Shared Kitchen campaign (`C-16EHE`) vs the general giving home.

---

## 12. Working on this with Claude Code

- Open this folder in VS Code; Claude Code can read `HANDOFF.md` + `index.html` and go.
- Single file to edit: `index.html` (CSS + JS are inline).
- After any change: regenerate `shared_kitchen_page.html` (§7), then the user re-pastes it into Squarespace.
- Before committing a visual change, preview locally **and** remember the Squarespace override rule (§6).
