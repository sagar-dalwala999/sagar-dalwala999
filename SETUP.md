# Profile README — setup

Everything in this folder goes into the repo named **`sagar-dalwala999`** (same as the username — that's what GitHub shows on the profile page).

## 1. Put the files in the repo

```
sagar-dalwala999/
├── README.md                 ← the profile
├── assets/                   ← 19 SVGs (hero, cards, buttons, stat cards…)
├── resume.pdf                ← TODO: add this (or change the link, see below)
└── .github/
    ├── workflows/snake.yml   ← contribution snake → `output` branch
    ├── workflows/cards.yml   ← nightly stats / languages / activity cards
    └── scripts/              ← the generator (edit content.py → re-run build.py)
```

Commit to `main`. If the repo's default branch is `master`, change `branches: [main]` in both workflows.

## 2. Fill the three TODOs

Search the repo for `TODO(sagar)`:

- `README.md` — two `href="#"` cards (Advanced RAG Agent, Crime Reporting PWA) → your repo URLs.
- `README.md` — the resume button → commit `resume.pdf` next to README, or point the href at a Drive/site link.
- `.github/scripts/content.py` — same three spots, so the generator stays in sync if you ever re-run it.

## 3. Let the workflows write to the repo

Repo **Settings → Actions → General → Workflow permissions → "Read and write permissions"** → Save.
Then **Actions tab → run "Contribution snake" and "Refresh profile cards" manually once** (Run workflow).
Until the first snake run finishes, the snake image in the README is a broken link — that's expected.

Optional: **Settings → Secrets → Actions → New secret `PROFILE_TOKEN`** with a classic PAT (scope `read:user`) if you want private contributions counted in the cards.

## 4. Editing later

- Change a project, a win, the stack, the about lines → edit `.github/scripts/content.py`, then
  `pip install -r .github/scripts/requirements.txt && python .github/scripts/build.py` and commit README.md + assets/.
- Change colours → `.github/scripts/palettes.py` (playful theme) or the `P` dict at the top of `style_theme.py` (lab theme), then re-run build.py.
- Hide the streak card → delete the one `streak-stats.demolab.com` line in README.md (there's a comment above it).
- Everything visual is an SVG in `assets/`; GitHub strips CSS/JS from READMEs, so styling has to live inside the images.

## Notes

- Text in the SVGs is converted to outlines — renders identically on every OS; no fonts are loaded by the browser.
- Fonts in `.github/scripts/fonts/` are under the SIL Open Font License / Apache 2.0; licences are included.
- Assets are tuned for GitHub dark mode. Light-mode viewers get readable but less pretty stickers.
- Stats, streak and snake show the activity of **sagar-dalwala999**; the featured cards link to the Sagar-Dalwala repos.
