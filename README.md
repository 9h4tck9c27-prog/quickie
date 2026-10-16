# Tonight's Deck

A short deck of bodyweight and dumbbell exercises, built for the evenings when
leaving the house is the thing standing between you and a workout.

Live at **https://tonights-deck.netlify.app**

## What it does

Deals a small session of exercise cards instead of showing a whole program.
Each card has a chalk-drawn diagram, a set/rep dose, and one form cue on the
back. Tap the card to flip it.

Three deck sizes:

| Deck | Cards | Roughly |
|------|-------|---------|
| Full deck | 6 | 25 min |
| Rough day | 3, easy variations only | 10 min |
| One card | 1 | 3 min |

The "Rough day" option is the point of the whole thing. On a bad evening the
choice becomes a small deck versus a big one, never a deck versus nothing.

A streak is tracked in `localStorage`, and a partial session still counts as a
day — a streak you can break by having one rough Tuesday stops being motivating
fast.

### Logging

Each card carries a row of set chips. They come prefilled with last session's
numbers and **one more on the first set**, because bodyweight work only keeps
working if it gets harder. The card shows what you did last time and your best.

Timed holds (plank, side plank, hollow body) get a count-up ring instead. Tap
to start, tap to stop, and the seconds drop straight into the set you just did.
The ring fills toward the target and turns green past it.

**History** shows a calendar of the last nine weeks plus a per-exercise row:
most recent sets, a sparkline of your best set per session, and your record.

### The mascot

The stick figure on the start screen picks a different routine every time the
app opens — jumping jacks, squats, push-ups, running laps, jump rope, sit-ups,
posing, burpees.

## Structure

Single self-contained `index.html`. No build step, no dependencies, no
framework — it runs from `file://` as happily as from a server. Fonts come from
Google Fonts; everything else is inline.

Places to edit:

- `F` — the SVG card figures, keyed by name, on a `0 0 220 132` viewBox
- `EX` — the exercise list (name, group, tier, dose, cue, `sets`, `start`, and
  `timed`/`target` for holds)
- `RECIPES` — which groups and tiers each deck size draws from
- `POSE` / `ROUTINES` — the mascot. A pose is 11 joints; a routine is a list of
  poses with a time on each, and the loop interpolates between them. Adding a
  routine is adding data, not code.

`tier: 1` is foundational, `tier: 2` is a harder progression. The "Rough day"
deck only ever draws tier 1.

To add an exercise, add a figure to `F` and an entry to `EX` pointing at it.
Nothing else needs touching — the deck builder picks from `EX` by group.

### Saved data

One `localStorage` key, `deck-state-v1`:

```
{ v, streak, last, history: [dates], total,
  log:  { exerciseId: [ { d: date, v: [sets] } ] },   // last 40 sessions each
  best: { exerciseId: topSet } }
```

Older saves without `log`/`best` are migrated in place on load, so a streak
from an earlier version survives.

## Deploying

Netlify builds from `main` on every push. There is no build command; the repo
root is published as-is.

```bash
git add -A
git commit -m "your change"
git push
```

## Adding it to a phone home screen

Open the site in Safari or Chrome, then Share → Add to Home Screen. The app
metadata in `<head>` makes it launch fullscreen with its own icon and no
browser chrome, so the gap between the thought and the first push-up is one tap.

## Note

The exercise form cues are general guidance, not individualized coaching.
