import json

with open("template_deck.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

for slide in slides:
    if "header" in slide and "title" in slide["header"]:
        template_name = slide.get("template", "UNKNOWN").upper()
        current_title = slide["header"]["title"]
        prefix = f"{template_name}: "
        if not current_title.startswith(prefix):
            slide["header"]["title"] = f"{prefix}{current_title}"

with open("template_deck.json", "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)
