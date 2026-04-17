# Static GitHub Pages Link Builder

When you share links to GitHub Pages on apps like WhatsApp, LinkedIn, or Slack, those platforms use a dumb scraper bot that only reads the raw `index.html` source code. They do not execute JavaScript, and therefore completely ignore the `?deck=...` instructions! This results in an ugly, generic link preview.

To solve this properly while keeping the benefits of simple GitHub Pages hosting, use the `build_decks.py` script.

## What it does
Instead of awkwardly sharing `https://ashishgupta-97065.github.io/Web_PPTs/?deck=999_Medcare_OS_9w39f7l1`, you will run the builder script. 

The script scans your `deck_jsons/` folder, extracts the specific Presentation Title and Subtitle from the JSON, and stamps out a physical standalone file called `999_Medcare_OS_9w39f7l1.html`. 

This new HTML file contains:
1. Hardcoded meta-tags containing the actual Title and Subtitle of that specific deck!
2. A Javascript injection so it instantly knows to load that correct JSON perfectly, exactly like before.

## How to use it
Every time you create a new deck or update the main Title of an existing deck:

1. Open your terminal in this folder (`998_Template`).
2. Run the script:
   ```bash
   python3 build_decks.py
   ```
3. You will immediately see new `.html` files generated in this root folder mapping to your json files.
4. Add, commit, and push them to GitHub:
   ```bash
   git add .
   git commit -m "Update static deck wrappers"
   git push
   ```

## Architecture: What lives where

| What you want to change | Where to change it |
|---|---|
| Slide content (title, subtitle, body text, cards) | `deck_jsons/<deck_name>.json` |
| Link preview on WhatsApp / LinkedIn (og:title, og:description) | `<deck_name>.html` wrapper **or** re-run `build_decks.py` |
| Styling / layout | `deck.css` |

> **Important:** The `.html` wrapper files are **thin shells** — they only hold OG meta tags and a script tag pointing to the JSON. They do **not** control what appears on screen. All visible slide content comes from the JSON. Each wrapper is deck-specific and standalone; editing one never affects another.

## Sharing the Link
Instead of sharing the old URL format, you will now just share the direct link to the auto-generated HTML file!

**Example Old URL:** `https://ashishgupta-97065.github.io/Web_PPTs/?deck=999_Medcare_OS_9w39f7l1`  
**Example New Built URL:** `https://ashishgupta-97065.github.io/Web_PPTs/999_Medcare_OS_9w39f7l1.html`

WhatsApp will crawl that exact HTML file and see accurate, rich preview metadata.
