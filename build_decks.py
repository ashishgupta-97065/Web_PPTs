import os
import json
import glob

def build_decks():
    # Directories
    JSON_DIR = "deck_jsons"
    STATIC_INDEX = "index.html"
    
    if not os.path.exists(JSON_DIR) or not os.path.exists(STATIC_INDEX):
        print(f"❌ Error: Make sure '{JSON_DIR}/' and '{STATIC_INDEX}' exist.")
        return

    # Read the base template once
    with open(STATIC_INDEX, "r", encoding="utf-8") as f:
        base_html = f.read()

    # Find all json decks
    json_files = glob.glob(os.path.join(JSON_DIR, "*.json"))
    
    if not json_files:
        print("⚠️ No JSON files found in deck_jsons/.")
        return

    print(f"🚀 Found {len(json_files)} presentations. Building custom HTML wrappers...")

    for json_path in json_files:
        basename = os.path.basename(json_path)
        deck_id = os.path.splitext(basename)[0]
        
        # Read the inner JSON to guess a good Title/Subtitle
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"  ❌ Error parsing {basename}: {e}")
                continue

        # Extract slides
        slides = data.get("slides", data)
        if not slides or not isinstance(slides, list):
            print(f"  ⚠️ No valid slides array in {basename}. Skipping.")
            continue
            
        # Try to find the title/subtitle from the first slide (usually Hero)
        first_header = slides[0].get("header", {})
        title = first_header.get("title", f"Presentation: {deck_id.replace('_', ' ')}")
        subtitle = first_header.get("subtitle", "View this interactive presentation")
        
        # We also might want to clean up single quotes to avoid html attribute breakages
        title = title.replace('"', '&quot;')
        subtitle = subtitle.replace('"', '&quot;')

        # Replace open graph metadata
        custom_html = base_html
        custom_html = custom_html.replace("<title>Presentation Deck</title>", f"<title>{title}</title>")
        custom_html = custom_html.replace('content="Presentation Deck"', f'content="{title}"')
        custom_html = custom_html.replace('content="View this interactive presentation"', f'content="{subtitle}"')

        # Dynamically inject the deck_id so Javascript knows what to load without ?deck=...
        # We replace: const deckName = urlParams.get('deck');
        # With: const deckName = urlParams.get('deck') || 'actual_deck_id';
        inject_target = "const deckName = urlParams.get('deck');"
        inject_replacement = f"const deckName = urlParams.get('deck') || '{deck_id}';"
        
        if inject_target in custom_html:
            custom_html = custom_html.replace(inject_target, inject_replacement)
        else:
            print(f"  ⚠️ Warning: Could not find js injection target in index.html for {deck_id}.")

        # Generate an output file based on the deck_id
        output_filename = f"{deck_id}.html"
        
        with open(output_filename, "w", encoding="utf-8") as out_f:
            out_f.write(custom_html)
            
        print(f"  ✅ Built: {output_filename} => Title: '{title[:30]}...'")

    print("\n🎉 All done! You can now share `https://ashishgupta-97065.github.io/Web_PPTs/FILENAME.html` directly!")

if __name__ == "__main__":
    build_decks()
