from markdownify import markdownify as md

def to_markdown(html: str) -> str:
    return md(
        html,
        heading_style="ATX",
        code_language_detection=True
    )
