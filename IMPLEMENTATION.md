# Squarespace implementation plan

Work top to bottom. Steps 1–3 are one-off setup; step 4 repeats per page.

---

## Before you start

**Check your plan tier.** Step 7 (the cursor) needs **Business or higher** — Code
Injection is not available on Personal. Everything else works on any plan.

**Check your version.** Settings → *Help* shows 7.0 or 7.1. This plan is written for
**7.1**. On 7.0 the Code Block still works but section padding differs, so expect to
nudge spacing.

**Duplicate the site first.** Squarespace can copy a whole site
(Settings → *Copy this site*). Do the work on the copy, review it, then repeat on the
live one — or set the copy live when it's ready. Do not learn this on the live site
during Compassion Camp registration.

---

## Step 1 · The design system, once

Design → **Custom CSS** → paste the whole of `shared/nspc-base.css` → Save.

That's the only global CSS. It is scoped to `.nspc-page`, so pages you haven't
converted yet are untouched and you can migrate one at a time.

**Do not paste `shared/nspc-chrome.css`.** See step 6.

---

## Step 2 · Upload the images

Every page references images by URL. Squarespace has no folder browser, so the trick is:

1. Make a throwaway page called `Image Library`, unlinked from navigation.
2. Add an Image Block for each file, upload it.
3. Click the image → the CDN URL is in the block's settings, or right-click →
   *Copy image address* on the published page.
4. Paste each URL over the placeholder in the page file.

Files to upload, from the repo:

| From | Used on |
|---|---|
| `pages/home/images/camp-treats.jpg` | Home, programme card 1 |
| `pages/home/images/camp-service-project.jpg` | Home, programme card 2 |
| `pages/home/images/camp-thank-you-cards.jpg` | Home, programme card 3 |
| `pages/*/images/hero.jpg` | placeholder heroes — **replace, don't upload** |

The `hero.jpg` files are stock landscapes from picsum.photos. They exist so layout
can be judged. Do not put them on the live site.

Search each page file for `PHOTO SLOT` to find every image that needs a real URL.

---

## Step 3 · Fix the broken URL slugs

Four live pages have slugs from being duplicated and never renamed:

| Current slug | Actually is | Should be |
|---|---|---|
| `/education-1` | Garden | `/garden` |
| `/education-1-1` | Congregational Life | `/congregational-life` |
| `/education-1-1-1` | Music | `/music` |
| `/ministries-3-2-1-2-1` | Contact | `/contact` |

Rename each in Page Settings, then add 301s so old links and search results survive:

Settings → Advanced → **URL Mappings**:

```
/education-1 -> /garden 301
/education-1-1 -> /congregational-life 301
/education-1-1-1 -> /music 301
/ministries-3-2-1-2-1 -> /contact 301
```

---

## Step 4 · Paste the pages

Per page: open it → delete existing content blocks → add a **Code Block** → paste the
whole of that page's `index.html` → Save.

Paste the file *including* its HTML comments. They carry the edit instructions and are
invisible to visitors.

| Repo file | Squarespace page | Slug |
|---|---|---|
| `pages/home/index.html` | Home | `/` |
| `pages/welcome/index.html` | Welcome | `/welcome` *(new)* |
| `pages/welcome/contact/index.html` | Contact | `/contact` |
| `pages/covenant-family/index.html` | Covenant Family | `/covenant-family` *(new)* |
| `pages/covenant-family/mission-and-values/index.html` | Mission and Values | `/mission-and-values` |
| `pages/covenant-family/neighboring-initiative/index.html` | Neighboring Initiative | `/neighboring-initiative` |
| `pages/covenant-family/leadership/index.html` | Leadership | `/leadership` |
| `pages/covenant-family/history/index.html` | History | `/history` |
| `pages/ministries/index.html` | Ministries | `/ministries` *(new)* |
| `pages/ministries/worship/index.html` | Worship | `/worship` |
| `pages/ministries/education/index.html` | Education | `/education` |
| `pages/ministries/garden/index.html` | Garden | `/garden` |
| `pages/ministries/congregational-life/index.html` | Congregational Life | `/congregational-life` |
| `pages/ministries/music/index.html` | Music | `/music` |
| `pages/ministries/shared-kitchen/index.html` | Shared Kitchen | `/shared-kitchen` |
| `pages/community-programs/index.html` | Community Programs | `/community-programs` *(new)* |
| `pages/community-programs/compassion-camp/index.html` | Compassion Camp | `/compassion-camp` ⚠ see step 9 |
| `pages/community-programs/after-school/index.html` | Kindness World Explorers | `/kindness-world-explorers` |
| `pages/community-programs/good-neighbour-exchange/index.html` | Good Neighbour Exchange | `/good-neighbour-exchange` |
| `pages/partnerships/index.html` | Partnerships | `/partnerships` *(new)* |
| `pages/partnerships/mission-partners/index.html` | Mission Partners | `/mission-partners` |
| `pages/partnerships/community-partners/index.html` | Community Partners | `/community-partners` |
| `pages/calendar/index.html` | Calendar | `/calendar` *(new)* |
| `pages/calendar/calendar-special-events/index.html` | Calendar & Special Events | `/calendar-special-events` |
| `pages/calendar/neighboring-initiative-events/index.html` | Neighboring Initiative Events | `/neighboring-initiative-events` |
| `pages/giving/index.html` | Giving | `/giving` *(new)* |
| `pages/giving/donations/index.html` | Donations | `/donations` |
| `pages/giving/capital-campaign/index.html` | Capital Campaign | `/capital-campaign` |

**Do one page first — Worship is a good test.** Check it, then do the rest. Do not
paste 28 pages and then start debugging.

### Page settings for each converted page

- **Page Header/Banner**: remove any banner image. The code block supplies its own hero.
- **Page title**: keep it for SEO and the browser tab, but Squarespace may also print it
  above your block. If it does, hide it per page with
  `Page Settings → Advanced → Page Header Code Injection`:
  `<style>.page-title,h1.entry-title{display:none}</style>`
- **Section padding**: set top and bottom padding to zero on the section holding the
  code block, or the hero will float in a gap.

---

## Step 5 · Turn the folders into landing pages

Seven nav items are currently Squarespace *folders*, which have no page of their own —
clicking them does nothing or opens the first child. The seven new pages in step 4
(`/welcome`, `/covenant-family`, `/ministries`, `/community-programs`,
`/partnerships`, `/calendar`, `/giving`) are those landing pages.

In the navigation panel, for each folder: add the new page as the **first item inside
it**, then set the folder to link to that page. On 7.1 that means dragging the page in
and using the folder's *Link* setting.

---

## Step 6 · Navigation and footer — configure, don't paste

**Do not paste `shared/header.html` or `shared/footer.html` into the site.** Squarespace
renders its own header and footer on every page. Pasting mine would give visitors two
of each.

Those two files exist so the previews can be judged in context. What they are *for* on
the live site is a **specification**: build Squarespace's own header and footer to match.

- **Header** — Design → *Header*. Set the logo, add the seven folders with the
  sub-pages listed in `shared/header.html`, and add a **Give** button linking to
  `https://secure.myvanco.com/L-ZMZZ/home`.
- **Footer** — edit the footer section directly. `shared/footer.html` has the content
  worth carrying across: address, phone, office hours, all three service times,
  section links, Facebook, and the PC(USA) line.

---

## Step 7 · The shepherd cursor — optional, do it last

Settings → Advanced → **Code Injection** → **Footer** → paste
`pages/home/cursor.html` → Save.

Homepage only instead: paste it into the homepage's
`Page Settings → Advanced → Page Header Code Injection`.

Before you commit to it, read the note in the file's header comment. Switching
`FIGURE = 'crook'` or `'pineapple'` is a one-word change.

---

## Step 8 · Three placeholders that are live right now

Independent of everything above, these are visible to visitors today:

1. **Leadership** shows *"session and deacons will look the same but I still need to
   get content."* Fixed by the new Leadership page.
2. **Calendar & Special Events** is a heading and the words *"Link to google calendar."*
   Fixed by the new Calendar pages — but you still need to paste your Google Calendar
   embed URL into `pages/calendar/calendar-special-events/index.html`.
   Calendar → ⋮ → *Settings and sharing* → tick *Make available to public* →
   *Integrate calendar* → copy the embed URL.
3. **Donations** shows `*LINK Copy Here`. Fixed by the new Donations page.
4. **News** still runs Squarespace's demo posts — three entries dated 5/28/2019 by
   "Allan Haas", each opening *"It all begins with an idea."* Delete all three in the
   blog editor. If you have nothing to replace them with, remove News from the
   navigation; an empty blog reads worse than no blog.

---

## Step 9 · Port the Compassion Camp registration form ⚠

**The rebuilt camp page cannot take registrations.** It describes camp and stops.

The working form lives only in
`pages/community-programs/compassion-camp/LIVE-with-registration-form.html` — the
current live page. It carries the field validation, the Vanco payment instructions,
and the Google Apps Script endpoint that writes submissions to your sheet.

**Do not replace the live Compassion Camp page until the form is ported across.** Camp
registration is open. Losing the form loses registrations.

Either keep the current page as-is for now, or treat the port as its own piece of work.

---

## Launch checklist

- [ ] One page converted and checked before the other 27
- [ ] Heroes span the full width, no horizontal scrollbar
- [ ] No duplicated page titles above the code blocks
- [ ] Every `PHOTO SLOT` has a real image, no picsum placeholders left
- [ ] `grep DUMMY` across `pages/` returns nothing
- [ ] Four broken slugs renamed, four 301s added
- [ ] Seven folders resolve to their landing pages
- [ ] Google Calendar embed URL added
- [ ] News demo posts deleted
- [ ] Compassion Camp form still working
- [ ] Tested on a phone — the drawer nav, the tilted photos, the century timeline
- [ ] Tested with a keyboard — every link reachable, focus visible
- [ ] Cursor: still usable if a visitor has it disabled

---

## Things that will go wrong

**The hero is a narrow column.** The section holding the code block has horizontal
padding. Set the section's padding to zero, or the `100vw` breakout fights it.

**A horizontal scrollbar appears.** `100vw` includes the scrollbar's width.
`.nspc-page{overflow-x:clip}` in the CSS handles it — check it survived the paste.

**Fonts look wrong.** The `@import` must be the *first* line of Custom CSS. CSS ignores
`@import` after any other rule. This bit us once already.

**Nothing is styled.** The page is missing its outer `<div class="nspc-page">`, or
`shared/nspc-base.css` didn't save. Every rule is scoped to that class.

**The century timeline stacks down one side.** Its milestones alternate by an explicit
`class="nspc-moment r"`. If you edit that section, keep alternating the class.

**Squarespace strips something.** Code Blocks allow HTML, CSS and JS, but the editor
can reformat on save. If a page breaks after an edit, re-paste from the repo rather
than fixing it in the editor.

---

## What is actually blocking a good result

Not the implementation — the photography. One worship photo for the whole site. Every
page in the reference set is carried by images of its own congregation, and this design
is built to showcase them. Get someone shooting a Sunday, the block party, the garden
beds, and staff headshots, and the site changes more than any further design work will.
