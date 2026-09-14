# Nate Chu's portfolio

A light, responsive biomedical-engineering portfolio for medtech and robotics employers. Hosted on GitHub Pages at https://lycoda.github.io/.

## Editing

- `index.html`: biography, academic record, selected-project summaries, experience and contact details.
- `content.json`: the detailed content and source links for all four project case studies.
- `scripts/render_projects.py`: regenerate the project HTML after editing `content.json` with `python scripts/render_projects.py`. Uses only the Python standard library. Commit the generated HTML; GitHub Pages needs no build step.
- `theme.css`: shared design tokens, page styles, responsive layouts, print and reduced-motion styles.
- `main.js`: progressive enhancement for the mobile menu, portrait reveal, animation control and section navigation.
- `fonts/`: self-hosted Instrument Sans and Public Sans, with their Open Font License files.
- `documents/`: academic source PDFs linked from the relevant case studies.

All articles and links are present in static HTML. JavaScript is optional for reading the site. The existing project URLs, hero imagery and CV path are retained.

## Preview

Run `python -m http.server 8765 --bind 127.0.0.1` in the repository and open http://127.0.0.1:8765/.

## Content provenance

The September 2026 revision uses the supplied fNIRS final dissertation, robotic-arm presentation summary, OsteoTrack group report and individual reflection, and REDCap form/scoring notes. The original site supplies the biography, qualifications and employment record. The REDCap internal form is summarised, not published. See `ASSETS.md` for imagery.

OsteoTrack is an academic concept; its report is labelled as a draft. fNIRS findings are reported with their selection-adjusted statistical limitations. Inconsistent robotic-arm accuracy and latency statements are qualified in the article. No clinical validation, funding secured or commercial deployment is implied.
