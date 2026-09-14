---
name: Nate Chu Portfolio
description: A light technical publication for biomedical engineering work.
colors:
  paper: "#f7f8fa"
  white: "#fff"
  ink: "#202c36"
  muted: "#586774"
  line: "#d9dfe4"
  blue: "#245dc1"
  blue-dark: "#174591"
  wash: "#edf1f5"
  article-ink: "#3e4f5e"
  table-ink: "#425361"
  control-border: "#b9c4ce"
  contact-wash: "#e9eef4"
typography:
  display:
    fontFamily: "'Instrument Sans', sans-serif"
    fontSize: "clamp(64px, 7.2vw, 96px)"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-.04em"
  case-display:
    fontFamily: "'Instrument Sans', sans-serif"
    fontSize: "clamp(38px, 5.2vw, 68px)"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-.025em"
  headline:
    fontFamily: "'Instrument Sans', sans-serif"
    fontSize: "clamp(28px, 3vw, 38px)"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-.025em"
  title:
    fontFamily: "'Instrument Sans', sans-serif"
    fontSize: "27px"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-.025em"
  body:
    fontFamily: "'Public Sans', sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  article:
    fontFamily: "'Public Sans', sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.85
  label:
    fontFamily: "'Public Sans', sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.7
  button:
    fontFamily: "'Public Sans', sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.4
rounded:
  control-media: "3px"
spacing:
  action-gap: "12px"
  inline-gap: "18px"
  body-gap: "20px"
  content-gap: "24px"
  heading-gap: "30px"
  group-gap: "32px"
  panel-padding: "36px"
  gutter: "40px"
  gutter-tablet: "28px"
  gutter-mobile: "22px"
  section: "82px"
  section-mobile: "54px"
components:
  button-primary:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.white}"
    typography: "{typography.button}"
    rounded: "{rounded.control-media}"
    padding: "12px 20px"
  button-primary-hover:
    backgroundColor: "{colors.blue-dark}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.control-media}"
    padding: "12px 20px"
  button-secondary-hover:
    backgroundColor: "{colors.wash}"
  project-image:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.control-media}"
  project-title:
    textColor: "{colors.ink}"
    typography: "{typography.title}"
  case-lead:
    backgroundColor: "{colors.wash}"
    padding: "36px"
  site-nav:
    textColor: "{colors.ink}"
  article-nav:
    textColor: "{colors.muted}"
  workflow:
    textColor: "{colors.ink}"
  table:
    textColor: "{colors.table-ink}"
---

# Design System: Nate Chu Portfolio

## Overview

**Creative North Star: "The Technical Publication"**

A biomedical engineering portfolio with the clarity of a technical publication. Cool paper, deep ink and precise blue actions give medtech and robotics employers a calm setting for examining real engineering work.

Generous reading space and hairline separators establish hierarchy. The retained portrait supplies the human, interactive moment; project figures and restrained metadata support the evidence.

**Key Characteristics:**

- Light, minimal and technical.
- Humanist typography with open reading space.
- Flat surfaces, quiet metadata and real project figures.

## Colors

A cool neutral field carries deep, legible text and one precise blue accent. Frontmatter values are normative.

### Primary

- **Precise Blue** (`blue`): primary actions, engineering subtitle, ECG mark, resource links and focus outlines.
- **Deep Blue** (`blue-dark`): primary action hover.

### Neutral

- **Cool Paper** (`paper`): page and sticky navigation background.
- **White** (`white`): figure stages and primary action text.
- **Deep Ink** (`ink`): headings and principal text.
- **Slate** (`muted`): descriptions, metadata and captions.
- **Hairline** (`line`): structural separators; **Control Border** outlines secondary actions.
- **Cool Wash** (`wash`): selected-project section, case-study lead and secondary action hover.
- **Article Ink** and **Table Ink**: long prose and data cells.
- **Contact Wash**: the quiet contact band.

**The Single Accent Rule.** Keep interface emphasis within the existing blue family; let project imagery retain its own colours.

## Typography

**Display Font:** Instrument Sans, with sans-serif fallback.  
**Body Font:** Public Sans, with sans-serif fallback.

Both are locally served at weights 400, 500, 600 and 700 with font-display swap. The pairing is clear and human, with tighter display spacing and relaxed prose. There is no separate monospace face or fixed modular scale.

- **Display:** the name on the homepage; **case-display:** project headline.
- **Headline:** homepage section headings; **title:** project-card headings.
- **Body:** general copy, normally capped at 72ch.
- **Article:** sustained reading, with a more generous line height.
- **Label:** quiet mixed-case metadata and captions; avoid badge styling.
- Article section headings use 30px; secondary article headings use 22px. Tables use tabular numerals.

## Layout

The centered container is capped at 1200px. Gutters step from 40px to 28px at 1000px, then 22px at 720px. Homepage sections use the section spacing tokens; heading rows meet a hairline separator.

Desktop composition uses an asymmetric hero (1.25fr / 1fr), two-column projects and open education/experience rows. Case studies use a three-column metadata line, a figure-and-summary lead, then a 240px contents rail beside a reading column capped at 740px. The rail is sticky at 120px; at 1000px it narrows to 185px.

At 720px and below, the hero, projects, case lead and article become single-column. Metadata becomes label/value rows; the contents moves above the article in two columns. The header changes from an 88px minimum to 76px and exposes a Menu control. Tables scroll inside their own focusable region.

The homepage name is 72px at the tablet breakpoint and 68px on mobile. Mobile case headlines are 40px, project titles 26px, and article copy 15px. At 1600px and above, hero vertical padding expands to 90px / 100px.

## Elevation & Depth

No box shadows are used. Depth comes from paper, wash and white figure surfaces, with thin separators and whitespace. The header is opaque and sticky. The portrait's layered reveal belongs to the imagery rather than the surrounding interface.

## Shapes

Controls, project image stages and the portrait have the small shared corner radius. Reading surfaces remain rectangular. Structural lines are 1px; there are no pill chips or floating cards. Arrows are small, open-stroke SVGs.

## Components

### Buttons and links

Primary and outlined secondary actions share the button tokens, a 48px minimum height and a 24px label-to-arrow gap. Hover darkens the primary or washes the secondary over 0.2s. Text links turn blue; eligible arrows move 3px over 0.2s. Keyboard focus uses a 3px blue outline offset by 5px.

### Navigation

The brand pairs a blue ECG line with the name and small discipline label. Desktop navigation is 13px with 30px gaps and 44px minimum link height. Mobile links are 14px and the menu closes on selection or Escape. Without JavaScript, navigation remains visible. Article contents links turn blue on hover and underline the current section.

### Project cards and case-study figures

Cards are open compositions: a white image stage, then title, category, description and project stage. Figures are contained without cropping by default; the robotic-arm photograph intentionally covers its stage. Image hover scales to 1.025 over 0.4s. Detailed figures keep captions and full-size links. The case-study lead uses a wash background and the panel-padding token, reduced to 22px on mobile.

### Tables and workflows

Tables use horizontal rules, left alignment, compact 13px text and tabular numerals. Numbered workflows use an open three-column sequence with muted descriptions and separators. Both tighten typography and spacing on mobile.

### Portrait reveal

The retained skeletal portrait reveals colour through a pointer-following radial mask, with a 0.35s opacity transition. Click, touch or keyboard activation pins the colour portrait; Escape restores the skeletal state. The reveal has an inset pale-blue focus outline. The ECG video has a pause control and pauses out of view or in a hidden tab.

Reduced motion removes transitions, image zoom and ECG playback, and leaves tap-to-switch portrait access. Print removes navigation and interactive controls and uses white paper, black text and underlined links.

## Do's and Don'ts

### Do:

- **Do** use blue for primary actions, links and visible keyboard focus.
- **Do** preserve readable figures, captions and source links.
- **Do** use spacing and hairline separators to organise long content.
- **Do** retain keyboard, touch and reduced-motion access to the portrait.

### Don't:

- **Don't** reintroduce dark instrumentation styling or decorative grids.
- **Don't** wrap every section in a bordered or elevated panel.
- **Don't** introduce pill badges or an unrelated display typeface.

