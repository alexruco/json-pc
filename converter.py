# html_jsonpc_converter.py
from bs4 import BeautifulSoup
import json

def extract_microdata_attributes(element):
    """Extract microdata attributes (itemscope, itemtype, itemprop) from an HTML element."""
    microdata = {}
    if element.has_attr("itemscope"):
        microdata["itemscope"] = True
    if element.has_attr("itemtype"):
        microdata["itemtype"] = element["itemtype"]
    if element.has_attr("itemprop"):
        microdata["itemprop"] = element["itemprop"]
    return microdata if microdata else None

def html_to_jsonpc(html):
    """Converts HTML to JSON-PC format."""
    soup = BeautifulSoup(html, 'html.parser')

    # Extract page-level metadata
    title_tag = soup.find('title')
    meta_desc_tag = soup.find('meta', attrs={"name": "description"})
    page_title = title_tag.get_text().strip() if title_tag else "Untitled"
    meta_description = meta_desc_tag["content"] if meta_desc_tag else ""
    slug = page_title.lower().replace(" ", "-")

    content_sections = []
    current_section = None
    current_text_lines = []

    def flush_text_block():
        nonlocal current_text_lines, current_section
        if current_text_lines:
            text = "\n".join(current_text_lines).strip()
            if text:
                block = {"type": "textBlock", "content": text}
                current_section["elements"].append(block)
            current_text_lines = []

    body = soup.find('body')
    if body is None:
        body = soup

    for elem in body.children:
        if elem.name is None:
            continue
        if elem.name == "h2":
            if current_section is not None:
                flush_text_block()
                content_sections.append(current_section)
            md = extract_microdata_attributes(elem)
            current_section = {
                "type": "section",
                "header": elem.get_text().strip(),
                "elements": []
            }
            if md:
                current_section["microdata"] = md
        elif elem.name == "p":
            current_text_lines.append(elem.get_text().strip())
        elif elem.name in ["ul", "ol"]:
            flush_text_block()
            md = extract_microdata_attributes(elem)
            list_items = [li.get_text().strip() for li in elem.find_all('li')]
            list_element = {"type": "list", "items": list_items}
            if md:
                list_element["microdata"] = md
            prev = elem.find_previous_sibling()
            if prev and prev.name == "h3":
                list_element["title"] = prev.get_text().strip()
            current_section["elements"].append(list_element)
        elif elem.name == "a":
            link = {
                "type": "link",
                "text": elem.get_text().strip(),
                "url": elem["href"],
                "target": elem.get("target", "self")
            }
            md = extract_microdata_attributes(elem)
            if md:
                link["microdata"] = md
            current_section["elements"].append(link)
        elif elem.name == "img":
            image = {
                "type": "image",
                "src": elem["src"],
                "alt": elem.get("alt", ""),
                "caption": elem.get("title", "")
            }
            md = extract_microdata_attributes(elem)
            if md:
                image["microdata"] = md
            current_section["elements"].append(image)
        elif elem.name == "video":
            video = {
                "type": "video",
                "src": elem["src"],
                "poster": elem.get("poster", ""),
                "caption": elem.get("title", "")
            }
            md = extract_microdata_attributes(elem)
            if md:
                video["microdata"] = md
            current_section["elements"].append(video)
        elif elem.name == "h3":
            flush_text_block()
            next_elem = elem.find_next_sibling()
            if next_elem and next_elem.name in ["ul", "ol"]:
                continue
            else:
                current_text_lines.append(elem.get_text().strip())

    if current_section is not None:
        flush_text_block()
        content_sections.append(current_section)

    if not content_sections and current_text_lines:
        content_sections.append({
            "type": "section",
            "header": "Content",
            "elements": [{"type": "textBlock", "content": "\n".join(current_text_lines).strip()}]
        })

    result = {
        "url": "",  # Can be set dynamically if needed
        "slug": slug,
        "title": page_title,
        "metaDescription": meta_description,
        "content": content_sections
    }
    return result

def jsonpc_to_html(jsonpc):
    """Converts JSON-PC to HTML format."""
    def format_microdata(md):
        if not md:
            return ""
        return " ".join([f'{k}="{v}"' if v is not True else k for k, v in md.items()])
    
    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"<title>{jsonpc.get('title', 'Untitled')}</title>",
        f'<meta name="description" content="{jsonpc.get("metaDescription", "")}">',
        "</head>",
        "<body>"
    ]
    for section in jsonpc.get("content", []):
        section_md = format_microdata(section.get("microdata"))
        html_lines.append(f"<h2 {section_md}>{section.get('header', '')}</h2>")
        for element in section.get("elements", []):
            if element.get("type") == "textBlock":
                block_md = format_microdata(element.get("microdata"))
                paragraphs = element.get("content", "").split("\n")
                for para in paragraphs:
                    para = para.strip()
                    if para:
                        html_lines.append(f"<p {block_md}>{para}</p>")
            elif element.get("type") == "list":
                if "title" in element:
                    list_title_md = format_microdata(element.get("microdata"))
                    html_lines.append(f"<h3 {list_title_md}>{element['title']}</h3>")
                html_lines.append("<ul>")
                for item in element.get("items", []):
                    html_lines.append(f"<li>{item}</li>")
                html_lines.append("</ul>")
            elif element.get("type") == "link":
                link_md = format_microdata(element.get("microdata"))
                target = ' target="_blank"' if element.get("target") == "blank" else ""
                html_lines.append(f'<a href="{element["url"]}"{target} {link_md}>{element["text"]}</a>')
            elif element.get("type") == "image":
                image_md = format_microdata(element.get("microdata"))
                html_lines.append(f'<img src="{element["src"]}" alt="{element["alt"]}" title="{element["caption"]}" {image_md}>')
            elif element.get("type") == "video":
                video_md = format_microdata(element.get("microdata"))
                html_lines.append(f'<video src="{element["src"]}" poster="{element["poster"]}" {video_md}></video>')
    html_lines.append("</body>")
    html_lines.append("</html>")
    return "\n".join(html_lines)

if __name__ == "__main__":
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page with Microdata</title>
        <meta name="description" content="This is a sample description.">
    </head>
    <body>
        <h2>Introduction</h2>
        <p>This is the first paragraph of the introduction.</p>
        <a href="https://example.com" target="_blank">Visit Example</a>
        <img src="https://example.com/image.jpg" alt="Sample Image">
    </body>
    </html>
    """
    jsonpc = html_to_jsonpc(sample_html)
    print("JSON-PC:")
    print(json.dumps(jsonpc, indent=2))
    html_output = jsonpc_to_html(jsonpc)
    print("\nReconstructed HTML:")
    print(html_output)