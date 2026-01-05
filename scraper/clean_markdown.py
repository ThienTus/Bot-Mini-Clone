import re

def slugify_anchor(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[’']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def clean_markdown(content: str) -> str:
    # Remove images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Fix undefined internal links → slugified anchors
    content = re.sub(
        r'\(https:\/\/support\.optisigns\.com\/hc\/.*?\/articles\/undefined#([^)]+)\)',
        lambda m: f"(#{slugify_anchor(m.group(1))})",
        content
    )

    # Remove markdown tables (IMPORTANT boxes)
    content = re.sub(
        r'\n\|.*?\|\n(?:\|.*?\|\n)+',
        '\n',
        content,
        flags=re.DOTALL
    )

    # Remove marketing/footer text
    marketing_patterns = [
        r'OptiSigns is the leader in.*',
        r'If you have any additional questions.*'
    ]
    for pattern in marketing_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

    lines = content.splitlines()
    cleaned = []

    for line in lines:
        line = line.rstrip()

        # Remove junk separators
        if line.strip() in ("****", "***"):
            continue

        # Fix duplicated heading hashes: "## # Title" → "## Title"
        line = re.sub(r'^(#+)\s*#+\s*', r'\1 ', line)

        # Normalize heading spacing
        line = re.sub(r'^(#+)([^ ])', r'\1 \2', line)

        cleaned.append(line)

    result = "\n".join(cleaned)

    # Normalize spacing
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip()
