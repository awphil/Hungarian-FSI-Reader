# Attribution & Sources

This project is an interactive interface built on top of publicly-available
Hungarian language-learning materials. It does not include, redistribute, or
modify those materials by default — you bring your own copy (see README).

## The course text and original audio

**FSI Hungarian Basic Course, Volume 1** — a U.S. Foreign Service Institute
language course produced by the U.S. government. As a work of the U.S.
government, it is in the **public domain** and freely redistributable.

- Canonical free home: <https://www.livelingua.com/fsi/Hungarian>
- Publisher: Foreign Service Institute, U.S. Department of State

## The Anki deck (segmentation + text alignment)

This reader is designed to work with the AnkiWeb shared deck
**"Hungarian FSI I Vocab and Basic Sentences"** by an independent contributor
who segmented the FSI audio tapes into individual sentence and vocabulary
clips and aligned them with text. That work makes the interactive click-to-play
experience possible.

- AnkiWeb page: <https://ankiweb.net/shared/info/124854924>

Thank you to that contributor. If you use this reader, please also visit the
AnkiWeb page above and consider thanking them there.

## What this repository provides

Only original code and styling:

- The React reader interface (`src/`)
- The Python build script (`scripts/`)
- Documentation and deployment configuration

**This repository does not distribute:**

- The FSI course text (bundled fresh from your Anki export at build time)
- The audio clips (bring-your-own; see README for hosting patterns)

