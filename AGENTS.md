# Instructions for AI Agents

This file gives coding agents (Claude Code, Codex, etc.) the context to work effectively in this repo. Read this before making changes.

## What this repo is

A **static** two-column reader for the FSI Hungarian Basic Course, Volume 1. There is no backend at runtime. A Python build script generates `public/reader.json` from a local Anki export; the React app loads it in the browser.

Do not add a server, database, or authentication layer. If a feature seems to need one, propose an alternative that keeps the site static.

## Architecture

```
scripts/build_reader_data.py    Python 3.11+, stdlib only. Reads Anki CSV → writes reader.json.
src/main.jsx                    React entry. Loads reader.json, renders the reader + audio player.
src/styles.css                  All styling. No CSS framework, no preprocessor.
public/                         Static assets served as-is (reader.json, local audio).
vite.config.js                  Build config. `base` and audio URL configured via env vars.
.github/workflows/deploy.yml    GitHub Pages deploy on push to main.
```

Frontend stack: React 19, Vite 6, lucide-react for icons. **No other dependencies.** If you need something new, justify it in the PR — this project values a tiny surface area.

Python: **standard library only** — the build script must run on a clean `python -3.11` with no `pip install`.

## Non-negotiable constraints

1. **No third-party audio or text in git.** The Anki CSV and audio files are user-supplied at build time. Never commit `.mp3`, `.wav`, `.apkg`, or Anki media directories. The `.gitignore` reflects this.
2. **Static site only.** No runtime server. No API calls out to services (analytics, telemetry, fonts, CDN JS). Everything the browser needs must ship in the build.
3. **Attribution stays.** The footer credits the AnkiWeb deck and the FSI course. Do not remove or hide these links.
4. **No auto-formatting churn.** If you edit a file, edit only the lines that need it. Do not reformat unrelated sections.

## Coding conventions

- **JSX:** function components, hooks, no class components. State lives in the component that uses it; no global store.
- **CSS:** BEM-ish class names (`fsi-row`, `fsi-hu`, `reader-toolbar`). Use CSS custom properties from `:root` for colors.
- **Python:** type hints where they clarify intent, docstrings on public functions, plain `argparse` for CLI.
- **Comments:** explain *why*, not *what*. If a comment restates the code, delete it.

## Testing changes

The Python build script has no automated tests in this repo (see the sibling [awphil/Learning-Hungarian](https://github.com/awphil/Learning-Hungarian) repo for coverage). If you change `build_reader_data.py`, run it end-to-end against a real Anki export and confirm `reader.json` still validates.

For frontend changes:
1. `npm run dev`
2. Verify: pagination top+bottom, hide/reveal per column, auto-play toggle persists via localStorage, audio plays at normal + slow speeds, mobile layout stacks correctly at 375px wide.

## Build & deploy quick reference

```bash
# Dev
npm install
python scripts/build_reader_data.py --anki-csv <csv> --media-dir <dir> --out public/reader.json
npm run dev

# Prod build (matches what CI does)
VITE_BASE_PATH=/Hungarian-FSI-Reader/ VITE_AUDIO_BASE_URL=https://.../ npm run build
```

## PR conventions

- One feature per PR. If you find an unrelated bug while working, note it in the PR description and leave it alone (or open a follow-up).
- Commit messages: imperative mood (`feat:`, `fix:`, `docs:`), one-line subject under 72 chars.
- Never commit `dist/`, `node_modules/`, `public/audio/`, `public/reader.json` (unless the maintainer has intentionally chosen to check in a dataset — check `.gitignore` first).

## When you're stuck or the request is ambiguous

Ask. Do not guess at requirements when a small clarifying question would resolve them. Especially avoid:
- Adding features "in case" they're useful later.
- Refactoring code that works to match a preferred style.
- Renaming things across the codebase for consistency you weren't asked to enforce.
