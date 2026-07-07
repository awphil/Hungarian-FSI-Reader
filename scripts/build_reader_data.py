"""Build the static reader.json from an Anki deck export.

The reader is deliberately data-driven: this script runs once at build time,
walks the Anki review CSV, and emits a single JSON file that the frontend
loads at page load. No Python is needed at runtime.

Usage (from repo root):

    python scripts/build_reader_data.py \\
        --anki-csv path/to/imported_apkg_review.csv \\
        --media-dir path/to/extracted_anki_media \\
        --out public/reader.json

You can also pass ``--deck "Some Deck Name"`` to select a specific deck when
the CSV holds multiple decks, and ``--rows-per-page N`` to override pagination.
The script does NOT copy audio files — see README for how to host them.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


DEFAULT_DECK = "Hungarian FSI I Vocab and Basic Sentences"
DEFAULT_ROWS_PER_PAGE = 24
READER_TITLE = "Hungarian FSI — Volume 1"

# Attribution shown in the reader footer. Edit if you build against a
# different deck or a different volume.
DEFAULT_SOURCE = {
    "deck": DEFAULT_DECK,
    "apkg": "FSI_Hungarian_I_Vocab__Basic_Sentences_with_audio.apkg",
    "course_name": "FSI Hungarian Basic Course (public domain)",
    "course_url": "https://www.livelingua.com/fsi/Hungarian",
    "anki_name": "Hungarian FSI I Vocab and Basic Sentences (AnkiWeb shared deck)",
    "anki_url": "https://ankiweb.net/shared/info/124854924",
}

_SENTENCE_END = re.compile(r"[.!?…]$")
_BILINGUAL_SEP = " / "


def classify(hungarian: str) -> str:
    """Return "sentence" if the Hungarian ends with sentence punctuation, else "vocab"."""
    text = (hungarian or "").strip()
    if not text:
        return "vocab"
    return "sentence" if _SENTENCE_END.search(text) else "vocab"


def split_bilingual(hungarian, english):
    """Split rows where the English is packed into the Hungarian field as
    "Hungarian / English" (a quirk of some Anki notes). Only splits when the
    English column is empty AND the separator appears.
    """
    hu = (hungarian or "").strip()
    en = (english or "").strip()
    if not en and _BILINGUAL_SEP in hu:
        left, _, right = hu.partition(_BILINGUAL_SEP)
        return left.strip(), right.strip()
    return hu, en


def load_rows(csv_path: Path, media_dir: Path, deck: str):
    """Load reader rows from the Anki review CSV, in textbook (note) order.

    Only rows whose audio file exists on disk are returned, so every row in
    the reader is guaranteed clickable-and-playable.
    """
    if not csv_path.is_file():
        raise SystemExit(f"CSV not found: {csv_path}")
    if not media_dir.is_dir():
        raise SystemExit(f"Media directory not found: {media_dir}")

    rows = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for raw in csv.DictReader(f):
            if raw.get("source_deck") != deck:
                continue
            hungarian, english = split_bilingual(
                raw.get("hungarian_text"), raw.get("english_text")
            )
            audio_file = (raw.get("audio_file") or "").strip()
            if not hungarian or not audio_file:
                continue
            if not (media_dir / audio_file).is_file():
                continue
            note_id = (raw.get("source_note_id") or "").strip()
            rows.append({
                "id": note_id or audio_file,
                "kind": classify(hungarian),
                "hungarian": hungarian,
                "english": english,
                "audio": audio_file,
            })

    def sort_key(item):
        try:
            return (0, int(item["id"]))
        except (ValueError, TypeError):
            return (1, 0)

    rows.sort(key=sort_key)
    return rows


def build_dataset(rows, rows_per_page, source):
    return {
        "title": READER_TITLE,
        "total_items": len(rows),
        "rows_per_page": rows_per_page,
        "source": source,
        "rows": rows,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anki-csv", type=Path, required=True,
                        help="Path to imported_apkg_review.csv (from your Anki export).")
    parser.add_argument("--media-dir", type=Path, required=True,
                        help="Path to the extracted Anki media directory.")
    parser.add_argument("--out", type=Path, default=Path("public/reader.json"),
                        help="Output path for reader.json (default: public/reader.json).")
    parser.add_argument("--deck", default=DEFAULT_DECK,
                        help=f"Anki deck name (default: {DEFAULT_DECK!r}).")
    parser.add_argument("--rows-per-page", type=int, default=DEFAULT_ROWS_PER_PAGE,
                        help=f"Rows per page (default: {DEFAULT_ROWS_PER_PAGE}).")
    args = parser.parse_args(argv)

    rows = load_rows(args.anki_csv, args.media_dir, args.deck)
    if not rows:
        raise SystemExit(
            f"No rows found for deck {args.deck!r}. Check --deck and that "
            f"audio files referenced in the CSV exist under {args.media_dir}."
        )

    source = {**DEFAULT_SOURCE, "deck": args.deck}
    dataset = build_dataset(rows, args.rows_per_page, source)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(dataset, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    print(f"Wrote {args.out} ({len(rows)} rows, {len(rows) // args.rows_per_page + 1} pages).")


if __name__ == "__main__":
    main()
