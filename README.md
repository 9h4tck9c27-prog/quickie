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

## Structure

Single self-contained `index.html`. No build step, no dependencies, no
framework. Fonts come from Google Fonts; everything else is inline.

Three places to edit:

- `F` — the SVG figures, keyed by name, drawn on a `0 0 220 132` viewBox
- `EX` — the exercise list (name, muscle group, tier, dose, form cue)
- `RECIPES` — which muscle groups and difficulty tiers each deck size draws from

`tier: 1` is foundational, `tier: 2` is a harder progression. The "Rough day"
deck only ever draws tier 1.

To add an exercise, add a figure to `F` and an entry to `EX` pointing at it.
Nothing else needs touching — the deck builder picks from `EX` by group.

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
