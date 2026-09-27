# My schedule

> Stretch myself to see how excellent I can be

A live 24-hour dial that shows the activity you are in **right now**, drawn as a
hand-made almanac. The clock opens on **your own time zone** and follows its
daylight-saving switch on its own.

No build step, no dependencies, no server. One HTML file.

Three tabs: **the plan** (the day you intend), **what I did** (the day as it
happened), and **insights** (what that adds up to).

## What it does

- **A 24-hour dial** — midnight at the top, noon at the bottom. Each block is a
  wedge; the one you are in fills up as it elapses, and a hand sweeps the day.
- **A sunflower at the centre** — a bud when a block begins, opening as the block
  runs, wide by the time it ends; when the next block takes over it folds back to
  a bud. It still leans the way the sun has gone, which is the hour rather than
  the block. The seed head is the surface the name and the countdown sit on.
  `targetBloom()` and `bloomTilt()` hold the curve, `animateSun()` handles the two
  moments you can actually watch — arriving, and a hand-over — and
  `sunflowerSVG()` draws it.
- **Right now** — the current activity, what time it ends, and how much is left.
- **Next up** — what follows and how long until it starts.
- **An editor** — name, start → end, and a colour you tap to cycle.
  Blocks may wrap past midnight, so `23:00 → 06:00` is a single block.
- **A time zone picker** — tap the clock line under the title. Every IANA zone is
  searchable, each row showing what time it is there now. Blocks are wall-clock
  times, not fixed instants: `09:00` means nine in the morning wherever you are,
  so the same routine reads correctly for everyone.
- **Watch the day** — the real dial turns a quarter of a degree a minute, which is
  no fun to look at, so this runs the same clock fast: 15 minutes, an hour or four
  hours every second. The hand sweeps, blocks hand over, and the flower blooms and
  folds. Nothing is faked — `preview.offset` is simply added to the time, and every
  reading follows from it. The stamp says `preview` while it runs.
- **Wallpaper** — a full-screen view, clock only. It asks for a screen wake
  lock so the phone stays lit.
- **Save as image** — exports a 1290 × 2796 print of the moment, laid out so the
  phone's own lock-screen clock doesn't cover anything. *(Only available in the
  Claude Artifact build — see below.)*

On a phone the page opens as the clock alone; the editor waits behind an
**edit blocks** button.

### what I did

The same dial, filled in after the fact. Log a block — an activity type and the
hours it really took — and open it for a to-do list: what you meant to get done
in those hours, ticked off as you go. Arrows at the top walk back through
earlier days.

The dial here is drawn the way the wallpaper is: seed spiral on the flower's
head, no hand, nothing written on it — a record rather than a clock. The bloom
itself is a gauge, opening with the share of your to-dos you have ticked off.
Hours logged and to-dos ticked are said in words under the dial.

**Activity types** are fixed in `DEFAULT_TYPES` — eight of them, offered in the
dropdown on every logged block. They are code, not saved state, so changing that
list changes the app everywhere at once. Ids are what entries store, so renaming
a category keeps its history; retiring one leaves its hours orphaned, and
`typeOf()` reads those as **Other** rather than as whatever sits first in the
list. `renderActual()` writes that correction back the first time the day is
opened.

### insights

**Daily**, **weekly** and **monthly**, each steppable backwards. It leads with
the story rather than the shapes: which activity took most of your time and how
that compares with the period before, how many days you actually wrote anything
down and which was fullest, your **productivity** — work logged against the
8 hours a day you mean to do — and whether the day was **balanced**.

Balance is three marks a day, held in `TARGETS`: at least 7 hours of sleep, about
an hour of projects, at least an hour of exercise. Clear all three and it says so;
miss one and it names which, by how much. Over a week or month the check runs on
your daily averages, and adds how many individual days hit all three.

Below that: where the time went (bars by activity for a day, stacked columns per
day for a week or month), one activity followed over time — a single day shows
the fortnight behind it, because one bar tells you nothing, trimmed to start
where your logging does so the bars fill the chart instead of hugging the right — and a table of
hours, share of logged time, share of the whole day and days active.

Both column charts carry a dashed **trend line** at their daily average, so every
bar reads as above or below a typical day. The average counts days that have
already happened, empty ones included, so an unlogged Monday pulls it down and a
Friday that has not arrived does not.

## Running it

Open `index.html` in a browser. That is the whole thing.

To put it on a phone, serve the folder over HTTP and open it there:

```bash
python3 -m http.server 8000
```

Or push to GitHub and turn on **Settings → Pages → Deploy from a branch**.
Then on the phone: **Share → Add to Home Screen**. The manifest and the Apple
meta tags make it open full-screen, without browser chrome.

## Sharing it

The **time zone is always per-person** — it lives in each visitor's own browser,
so two people looking at the same page can each read it in their own local time
without touching each other's view. It defaults to the zone their device reports.

The **blocks** are shared, and the two builds differ:

- **This repo, hosted anywhere.** Everyone who opens the link gets their own
  private copy in their own browser. They can edit freely; nothing they do
  reaches anyone else, and nothing reaches you. The blocks they start from are
  `DEFAULT_BLOCKS` in `schedule.html`, so put your own routine there before you
  publish if you want to share yours.
- **The Claude Artifact.** One shared set of blocks, backed by the artifact's
  database. Only people you give *Can edit* to may change them; everyone else
  sees the schedule read-only and the editor says so. Artifacts that use that
  database are limited to your organisation, so a link for the wider world means
  the hosted build above.

## Where your blocks are stored

| Build | Plan, log and types | Time zone, open tab |
| --- | --- | --- |
| `index.html` (this repo) | `localStorage`, per browser | `localStorage`, per browser |
| Claude Artifact | the artifact's shared database, so edits follow you across devices | `localStorage`, per browser |

In the Artifact build the plan lives at `schedule/main`, the activity types at
`settings/types`, and each logged day at `days/YYYY-MM-DD` — one document per
day, so a year of logging is 365 of the database's 5,000 documents. Dates are
plain `YYYY-MM-DD` strings in your chosen zone, and the arithmetic on them runs
in UTC, so a daylight-saving jump can never skip or repeat a day.

The page checks for `window.claude` at load. When it isn't there — which is the
case for every ordinary web host — it falls back to `localStorage` and hides the
PNG export, since a sandboxed page can't hand the browser a file on its own.

## The two HTML files

`schedule.html` is the source: the page body only. It is written for the Claude
Artifact viewer, which wraps it in a document skeleton (doctype, charset,
viewport, a small reset) at publish time.

`index.html` is that same page wrapped in a real document so it works on any
web server. It is **generated** — edit `schedule.html`, then:

```bash
python3 build.py
```

## Making it yours

Everything is in `schedule.html`.

- **The starting time zone** — `HOME_TZ` near the top of the script. It is only a
  fallback: the page prefers what the visitor's device reports, and then whatever
  they last picked. `COMMON_TZ` is the shortlist shown before anyone searches,
  and `TZ_ALIAS` maps the legacy ids browsers still return (`Asia/Saigon`,
  `Asia/Calcutta`, `Europe/Kiev`) onto the names people actually type.
- **Starter blocks** — `DEFAULT_BLOCKS`. Times are minutes past midnight, `c` is
  a palette slot 1–8. They only show until you edit something.
- **Colours** — the `--c1` … `--c8` tokens in `:root`, redefined for dark mode
  in the two blocks below it.
- **Type** — Cormorant Garamond for display (tiny, letterspaced, lowercase) and
  EB Garamond for reading. Both from Google Fonts. The hierarchy is deliberately
  flat and small: the dial is the loudest thing on the page, not the words.
- **Botany** — `BOT` holds the plants (clover, grass, daisy, tulip, buds) as SVG
  path builders; `plant()` places one, `wash()` lays down a watercolour pool.
  `marginalia()` arranges the garden in the dial's empty corners. The faint
  pencil sketches behind everything are the `--sketchtile` background.
- **The painted look** is not a filter. Every arc and edge is sampled through
  `warp()`, a deterministic wobble keyed to radius and angle, so neighbouring
  wedges land on identical points and meet with no gaps. Each block is filled
  twice with different seeds, so the washes pool where they overlap, the way
  watercolour does. `bandRings()` and `arcPts()` do the work, and the PNG export
  reuses them, so the exported image wobbles exactly like the page.

## Licence

Yours to do whatever you like with.
