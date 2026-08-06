# northshorepres.org rebuild

## How this works

```
shared/nspc-base.css        design system — paste ONCE into Design → Custom CSS
pages/<section>/index.html  one code block per nav section
pages/<section>/reference/  ← drop your reference designs, photos, notes here
```

Each `pages/<section>/index.html` is a **section landing page** covering everything
in that nav folder, rather than a page per sub-page. That's the pattern your
reference sites use — Cedarcrest avoids submenus by linking to landing pages —
and it means eight pages to maintain instead of twenty-six.

Drop anything into `reference/` and I'll build against it: screenshots of sites you
like, photographs, a scan of the bulletin, notes. Filenames don't matter.

## Build order

| # | Section | Covers | Status |
|---|---|---|---|
| 1 | Home | — | ✅ approved |
| 2 | Covenant Family | Mission & Values, Neighboring Initiative, Leadership, History | ✅ built |
| 3 | Ministries | Worship, Education, Garden, Congregational Life, Music, Shared Kitchen | ⚠️ needs content |
| 4 | Community Programs | Compassion Camp, After School, Good Neighbour Exchange | ready to build |
| 5 | Partnerships | Mission Partners, Community Partners | ready to build |
| 6 | Calendar | Calendar & Special Events, Neighboring Initiative Events | needs calendar URL |
| 7 | Welcome / Contact | Contact | ⚠️ needs content |
| 8 | Giving / Donate | Donations, Capital Campaign | ⚠️ needs content |

## Three placeholders are live on the public site right now

These are visible to visitors today. All three are fixed by the pages above, but
worth knowing they're out there:

- **Leadership** — "session and deacons will look the same but I still need to get content"
- **Calendar & Special Events** — the page is a heading and the words "Link to google calendar"
- **Donations** — displays `*LINK Copy Here`

Separately, the **News** page still runs Squarespace's demo posts: three entries dated
5/28/2019 by "Allan Haas", each beginning *"It all begins with an idea."* Delete them in
the blog editor, or drop News from the nav.

## What I still need

**Ministries (section 3)** — two of six answered themselves via the Mission Partners page:
- ~~Garden~~ — 6 raised beds, produce to Apostle Presbyterian Food Pantry, part of Food for the Journey ✅
- ~~Shared Kitchen~~ — "Gather and Grow", commercial-grade upgrade, rentable to local food entrepreneurs ✅
- **Music** — what ensembles exist, when do they rehearse, how does someone join?
- **Congregational Life** — beyond "Ladies Who Lunch" and Interfaith Thanksgiving, what else, and how to join?

**Giving (section 8)** — is there a capital campaign running? Goal, purpose, progress?
Right now that page is empty and Donations is a placeholder.

**Welcome / Contact (section 7)** — office hours, parking, accessibility, who to call for what.

## Photography — the thing that matters most

The site has **one photograph**: the worship shot, reused everywhere. Every reference
site you sent is carried by dozens — faces, hands, the garden beds, coffee hour, the
block party, the choir.

This design showcases photography, which means it gets thinner the further it runs from
that single image. Staff circles are initials because there are no headshots.

If someone can shoot one Sunday morning and one block party, the whole site changes.
Everything else is a smaller lever than this.

## Publishing

Pages reference images by their Squarespace CDN URLs, so they work as-is once pasted.
I can't publish to Squarespace — that needs your admin login.
