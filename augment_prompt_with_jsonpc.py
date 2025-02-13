

def augment_prompt_with_jsonpc(prompt: str, type: str) -> str:
    common_instruction = (
        "The JSON-PC format includes the following keys:\n"
        "- 'url': the page URL\n"
        "- 'slug': a URL-friendly identifier\n"
        "- 'title': the page title\n"
        "- 'metaDescription': a short SEO description\n"
        "- 'content': an array of sections, where each section includes:\n"
        "   - 'type': should be 'section'\n"
        "   - 'header': section title (e.g., from h2 element)\n"
        "   - 'microdata' (optional): microdata attributes\n"
        "   - 'elements': an array of elements. Supported elements include:\n"
        "       * 'textBlock': multi-paragraph text\n"
        "       * 'list': with a title and items (e.g., from ul or ol)\n"
        "       * 'image': with src, alt, and caption\n"
        "       * 'video': with src, poster, and caption\n"
        "       * 'link': with text, url, and target ('blank' or 'self')\n"
        "       * 'faq': with questions and answers\n"
        "Please ensure that your output is valid JSON following the JSON-PC specification."
    )

    if type == "response":
        jsonpc_instruction = (
            "Your response must be in JSON-PC, a structured JSON format for webpage content. "
            + common_instruction
        )
    elif type == "question":
        jsonpc_instruction = (
            "The provided content is JSON-PC, a structured JSON format for webpage content. "
            + common_instruction
        )
    else:
        raise ValueError("Invalid type. Expected 'response' or 'question'.")

    return f"{prompt.strip()}\n\n{jsonpc_instruction}"
