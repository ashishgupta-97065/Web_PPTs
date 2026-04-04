import json

with open("template_deck.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

templates = {}
for slide in slides:
    tmpl = slide.get("template", "Unknown")
    if tmpl not in templates:
        templates[tmpl] = []
    templates[tmpl].append(slide)

kept_slides = []
for tmpl, group in templates.items():
    if tmpl == "Unknown": continue # Skip unknown if any
    
    # Heuristic for "most details" is number of structural keys, then length of JSON
    best_slide = max(group, key=lambda s: (len(s.keys()), len(json.dumps(s))))
    kept_slides.append(best_slide)

# Sort back by original sequential ID so the presentation flows somewhat naturally
kept_slides.sort(key=lambda s: int(s["id"].replace("s", "")))

with open("template_deck.json", "w", encoding="utf-8") as f:
    json.dump(kept_slides, f, indent=2, ensure_ascii=False)

print(f"Filtered down to {len(kept_slides)} unique templates:")
for s in kept_slides:
    print(f"- {s['template']} (Slide {s['id']})")
