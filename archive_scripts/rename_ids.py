import json

with open("template_deck.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

for i, slide in enumerate(slides):
    slide['id'] = f"slide{i+1}"

with open("template_deck.json", "w", encoding="utf-8") as f:
    json.dump(slides, f, indent=2, ensure_ascii=False)
