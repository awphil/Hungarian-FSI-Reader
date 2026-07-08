# Hungarian FSI Reader

**[Try it live →](https://awphil.github.io/Hungarian-FSI-Reader/)**

An interactive two-column book reader for the **FSI Hungarian Basic Course, Volume 1**. Every Hungarian line is a click-to-play audio button, English and Hungarian columns can be hidden independently, and hidden cells reveal one at a time so you can self-test.

The reader is a **static site**: a Python build script turns your Anki export into a single `reader.json`, and the React app loads it in the browser. There is no server at runtime — it deploys to GitHub Pages (or any static host) with `git push`.

## What you get

- Two-column layout matching the textbook (English | Hungarian, vocab entries indented under their sentence).
- Click any Hungarian line to play its recording, at normal or 0.75× speed.
- Hide either column and reveal cells one at a time — with optional auto-play on reveal.
- Page navigation top and bottom, 24 items per page, breaks only after a completed sentence.
- Persistent settings via `localStorage`; no accounts, no backend.

## Prerequisites

You need three things before you can run this:

1. **Node 20+** and **Python 3.11+** on your machine.
2. **The Anki deck** ["Hungarian FSI I Vocab and Basic Sentences"](https://ankiweb.net/shared/info/124854924) imported into Anki, with its audio media extracted. See **[Getting the data](#getting-the-data)** below.
3. **Somewhere to host the audio.** The default is a GitHub Release on this same repo (recommended, free, no extra accounts). See **[Deployment](#deployment)**.

The reader is **bring-your-own-audio**: no clips ship in this repo. Audio and text come from third parties (see [ATTRIBUTION.md](ATTRIBUTION.md)); you export them yourself from the Anki deck.

## Getting the data

1. Install Anki desktop and add the shared deck [Hungarian FSI I Vocab and Basic Sentences](https://ankiweb.net/shared/info/124854924).
2. Export the deck as a `.apkg` with media included (File → Export → check "Include media").
3. Unzip the `.apkg` (it's a zip archive). You'll get two useful things:
   - A `collection.anki2` SQLite database with the notes.
   - Media files with numeric names, plus a `media` mapping file.
4. Convert that into the CSV this build script expects — a single file with columns `source_deck`, `source_note_id`, `hungarian_text`, `english_text`, `audio_file`, and rename media files to their real names using the `media` mapping.

If you already have an `imported_apkg_review.csv` from a previous project (this is the format used by the sibling [awphil/Learning-Hungarian](https://github.com/awphil/Learning-Hungarian) pipeline), you can use it directly.

## Local development

```bash
# Install
npm install

# 1. Build the reader dataset from your local Anki export
python scripts/build_reader_data.py \
    --anki-csv /path/to/imported_apkg_review.csv \
    --media-dir /path/to/extracted_anki_media \
    --out public/reader.json

# 2. Put audio files where the dev server can serve them
mkdir -p public/audio
cp /path/to/extracted_anki_media/*.mp3 public/audio/

# 3. Run the dev server
npm run dev
```

Open `http://localhost:5173/`. Edits to `src/` hot-reload; edits to `reader.json` require a page refresh.

## Deployment

The recommended pattern is **GitHub Pages for the site + GitHub Releases for the audio**. Everything is free and lives in this one repo — no external accounts.

### 1. Publish the audio as a release

From the local Anki media directory (large — 100+ MB), create a Release and attach the audio files. The `gh` CLI makes this easy:

```bash
# From a directory containing the audio files
gh release create audio-v1 --title "Audio v1" --notes "FSI Hungarian audio" *.mp3 *.wav
```

The exact URL prefix will be:
```
https://github.com/<USER>/<REPO>/releases/download/audio-v1/
```

### 2. Point the build at that URL

In your repo settings, add a repository **variable** (Settings → Secrets and variables → Actions → Variables → New repository variable):

- Name: `AUDIO_BASE_URL`
- Value: `https://github.com/<USER>/<REPO>/releases/download/audio-v1/` (must end with `/`)

The provided GitHub Actions workflow reads this variable at build time.

### 3. Commit reader.json

The build script generates `public/reader.json`. Commit it (it's the data your deployed site loads):

```bash
python scripts/build_reader_data.py \
    --anki-csv /path/to/imported_apkg_review.csv \
    --media-dir /path/to/extracted_anki_media \
    --out public/reader.json

git add public/reader.json
git commit -m "data: rebuild reader.json"
```

Note: `.gitignore` currently excludes `public/reader.json` to keep it out of the repo by default. Remove that line (or force-add with `git add -f`) once you're happy with the dataset.

### 4. Enable GitHub Pages

In Settings → Pages, set the Source to **GitHub Actions**. Push to `main` and the workflow at `.github/workflows/deploy.yml` will build and publish to `https://<USER>.github.io/<REPO>/`.

### Alternative hosts

The site is a plain static build under `dist/`. Any static host works (Netlify, Cloudflare Pages, S3+CloudFront, your own web server). Just set `VITE_BASE_PATH` and `VITE_AUDIO_BASE_URL` when you build.

## Building for another volume or language

The reader is language-agnostic — only two things are Hungarian-specific:

1. The `_SENTENCE_END` regex in [scripts/build_reader_data.py](scripts/build_reader_data.py:38) — `[.!?…]$`. If your source uses different terminal punctuation, adjust it.
2. The attribution text (`DEFAULT_SOURCE` in the same file) — change to match your source deck.

To build a Volume 2 reader, or a Spanish FSI reader, or any other Anki deck that pairs a foreign-language field with an English gloss and an audio file:

```bash
python scripts/build_reader_data.py \
    --anki-csv /path/to/other-deck.csv \
    --media-dir /path/to/other-media \
    --deck "Your Deck Name" \
    --out public/reader.json
```

The column names the script reads (`source_deck`, `hungarian_text`, `english_text`, `audio_file`) may need renaming in the script if your CSV differs — one edit at the top of `load_rows()`.

## Attribution

The FSI Hungarian Basic Course is US-government public domain material. The Anki deck that segments and aligns the audio is the work of an independent contributor on AnkiWeb. See [ATTRIBUTION.md](ATTRIBUTION.md) for full credits and please thank the deck author.

## Repo structure

```
src/            React reader (main.jsx, styles.css)
scripts/        Python build script (build_reader_data.py)
public/         Static assets (reader.json, audio for local dev)
.github/workflows/  GitHub Pages deploy
AGENTS.md       Instructions for AI agents working in this repo
ATTRIBUTION.md  Credits for the FSI course + AnkiWeb deck
```
