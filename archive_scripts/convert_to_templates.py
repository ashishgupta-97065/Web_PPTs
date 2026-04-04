import json

with open("deck.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

new_slides = []

def extract_text(node):
    if isinstance(node, dict):
        if 'text' in node:
            return node['text']
        if 'children' in node:
            return " ".join([extract_text(c).strip() for c in node['children'] if extract_text(c).strip()])
    return ""

def get_header(elements):
    tag_node = next((n for n in elements if n.get('class') and 'tag' in n.get('class') and n.get('tag') == 'span'), None)
    h1_node = next((n for n in elements if n.get('tag') in ['h1', 'h2']), None)
    sub_node = next((n for n in elements if n.get('class') == 'sub'), None)
    
    header = {}
    if tag_node:
        header['tag'] = extract_text(tag_node).strip()
        classes = tag_node.get('class', '').split()
        if len(classes) > 1 and 'tag-' in classes[1]:
            header['tagColor'] = classes[1].replace('tag-', '')
        else:
            header['tagColor'] = 'default'
    if h1_node:
        header['title'] = extract_text(h1_node).strip()
    if sub_node:
        header['subtitle'] = extract_text(sub_node).strip()
    return header

for slide in slides:
    new_slide = {
        "id": slide["id"],
        "template": "Unknown",
        "theme": "light",
        "header": {}
    }
    
    css = slide.get('classes', '')
    if 'slide-dark' in css: new_slide['theme'] = 'dark'
    elif 'slide-teal' in css: new_slide['theme'] = 'teal'
        
    elements = slide.get('elements', [])
    sid = slide["id"]
    
    if sid in ["s0", "s1", "s24"]:
        new_slide["template"] = "Hero"
        content_div = elements[0].get('children', []) if elements else []
        new_slide["header"] = get_header(content_div)
        p_nodes = [extract_text(n) for n in content_div if n.get('tag') == 'p' and not ('sub' in n.get('class', ''))]
        new_slide["content"] = p_nodes
        
    elif sid in ["s2", "s3", "s4", "s14", "s15", "s16"]:
        new_slide["template"] = "Process"
        new_slide["header"] = get_header(elements)
        steps = []
        step_nodes = [n for n in elements if n.get('class') == 'step' or (n.get('class') and 'step ' in n.get('class'))]
        for step in step_nodes:
            ch = step.get('children', [])
            step_n = next((n for n in ch if n.get('class') and 'step-n' in n.get('class')), None)
            step_num = extract_text(step_n).strip() if step_n else ""
            step_color = "default"
            if step_n and 'red' in step_n.get('class', ''): step_color = 'red'
            
            step_content_div = next((n for n in ch if n.get('tag') == 'div' and n != step_n), None)
            step_data = {"number": step_num, "color": step_color, "heading": "", "text": []}
            
            if step_content_div:
                c_ch = step_content_div.get('children', [])
                h4 = next((n for n in c_ch if n.get('tag') == 'h4'), None)
                if h4: step_data["heading"] = extract_text(h4).strip()
                p_nodes = [n for n in c_ch if n.get('tag') == 'p']
                step_data["text"] = [extract_text(p).strip() for p in p_nodes]
                
                step_detail = next((n for n in c_ch if n.get('class') == 'step-detail' or (n.get('class') and 'step-detail ' in n.get('class'))), None)
                if step_detail:
                    step_data["details"] = []
                    for col in step_detail.get('children', []):
                        if col.get('tag') == 'div':
                            col_ch = col.get('children', [])
                            d_h5 = next((n for n in col_ch if n.get('tag') == 'h5'), None)
                            tags = [extract_text(n) for n in col_ch if n.get('class') and 'ch-tag' in n.get('class')]
                            d_p = next((n for n in col_ch if n.get('tag') == 'p'), None)
                            det = {"title": extract_text(d_h5).strip() if d_h5 else ""}
                            if tags: det["tags"] = tags
                            if d_p: det["text"] = extract_text(d_p).strip()
                            step_data["details"].append(det)
            steps.append(step_data)
        new_slide["steps"] = steps
        
    elif sid in ["s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s17", "s19", "s20"]:
        new_slide["template"] = "GridCards"
        new_slide["header"] = get_header(elements)
        grids = [n for n in elements if n.get('class') and n.get('class').startswith('grid')]
        new_slide["grids"] = []
        for g in grids:
            grid_type = g.get('class').split()[0]
            grid_cards = []
            for c in g.get('children', []):
                if c.get('class') and 'card' in c.get('class'):
                    card_h4 = next((n for n in c.get('children', []) if n.get('tag') == 'h4'), None)
                    card_p = [n for n in c.get('children', []) if n.get('tag') == 'p']
                    # grab emojis or top styles if possible
                    card_top = next((n for n in c.get('children', []) if n.get('class') and 'card-top' in n.get('class')), None)
                    theme = 'light' if 'card-dark' not in c.get('class') else 'dark'
                    grid_cards.append({
                        "theme": theme,
                        "heading": extract_text(card_h4).strip() if card_h4 else "",
                        "text": [extract_text(p).strip() for p in card_p]
                    })
            new_slide["grids"].append({
                "type": grid_type,
                "cards": grid_cards
            })
            
    elif sid == "s18":
        new_slide["template"] = "BeforeAfter"
        new_slide["header"] = get_header(elements)
        bas = [n for n in elements if n.get('class') and 'ba ' in n.get('class') or n.get('class') == 'ba'] 
        comparisons = []
        for ba in bas:
            b_node = next((n for n in ba.get('children', []) if n.get('class') and 'ba-before' in n.get('class')), None)
            a_node = next((n for n in ba.get('children', []) if n.get('class') and 'ba-after' in n.get('class')), None)
            
            comp = {"before": {}, "after": {}}
            if b_node:
                b_h5 = next((n for n in b_node.get('children', []) if n.get('tag') == 'h5'), None)
                b_p = next((n for n in b_node.get('children', []) if n.get('tag') == 'p'), None)
                comp["before"] = {"heading": extract_text(b_h5).strip() if b_h5 else "", "text": extract_text(b_p).strip() if b_p else ""}
            if a_node:
                a_h5 = next((n for n in a_node.get('children', []) if n.get('tag') == 'h5'), None)
                a_p = next((n for n in a_node.get('children', []) if n.get('tag') == 'p'), None)
                comp["after"] = {"heading": extract_text(a_h5).strip() if a_h5 else "", "text": extract_text(a_p).strip() if a_p else ""}
            comparisons.append(comp)
        new_slide["comparisons"] = comparisons
        
    elif sid == "s21":
        new_slide["template"] = "Timeline"
        new_slide["header"] = get_header(elements)
        tls = [n for n in elements if n.get('class') and ('tl ' in n.get('class') or n.get('class') == 'tl')]
        items = []
        if tls:
            for item in tls[0].get('children', []):
                if item.get('class') == 'tl-item':
                    h4 = next((n for n in item.get('children', []) if n.get('tag') == 'h4'), None)
                    dur = next((n for n in item.get('children', []) if n.get('class') == 'dur'), None)
                    p = next((n for n in item.get('children', []) if n.get('tag') == 'p'), None)
                    items.append({
                        "heading": extract_text(h4).strip() if h4 else "",
                        "duration": extract_text(dur).strip() if dur else "",
                        "text": extract_text(p).strip() if p else ""
                    })
        new_slide["timeline"] = items
        
    elif sid in ["s22", "s23"]:
        new_slide["template"] = "TableLayout"
        new_slide["header"] = get_header(elements)
        
        t = next((n for n in elements if n.get('tag') == 'table'), None)
        if not t:
            for el in elements:
                if el.get('tag') == 'div' and el.get('children'):
                    t = next((n for n in el.get('children', []) if n.get('tag') == 'table'), None)
                    if t: break

        table_data = {"headers": [], "rows": []}
        if t:
            thead = next((n for n in t.get('children', []) if n.get('tag') == 'thead'), None)
            tbody = next((n for n in t.get('children', []) if n.get('tag') == 'tbody'), None)
            
            if thead:
                tr = next((n for n in thead.get('children', []) if n.get('tag') == 'tr'), None)
                if tr:
                    table_data["headers"] = [extract_text(th).strip() for th in tr.get('children', []) if th.get('tag') == 'th']
            if tbody:
                for tr in tbody.get('children', []):
                    if tr.get('tag') == 'tr':
                        row = [extract_text(td).strip() for td in tr.get('children', []) if td.get('tag') == 'td']
                        table_data["rows"].append(row)
        new_slide["table"] = table_data
        
        grid3 = next((n for n in elements if n.get('class') == 'grid3' or (n.get('class') and 'grid3 ' in n.get('class'))), None)
        if grid3:
            grid_cards = []
            for c in grid3.get('children', []):
                if c.get('class') and 'card' in c.get('class'):
                    p_nodes = [n for n in c.get('children', []) if n.get('tag') == 'p']
                    grid_cards.append([extract_text(p).strip() for p in p_nodes])
            new_slide["grid"] = grid_cards

    new_slides.append(new_slide)

with open("template_deck.json", "w", encoding="utf-8") as f:
    json.dump(new_slides, f, indent=2, ensure_ascii=False)
