from zendesk import fetch_articles
from markdown import to_markdown
from clean_markdown import clean_markdown
from upload_to_openai import upload_changed_files

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime

# --- PATHS ---
OUTPUT = Path("output/articles")
STATE_FILE = Path("state/articles.json")
LOG_FILE = Path("logs/dailyjob.log")

OUTPUT.mkdir(parents=True, exist_ok=True)
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# --- HELPERS ---
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_state():
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def log(msg: str):
    line = f"[{datetime.utcnow().isoformat()}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# --- MAIN ---
def main():
    log("=== Daily scrape job started ===")

    old_state = load_state()
    new_state = {}

    added = updated = skipped = 0
    changed_files = []

    articles = fetch_articles(30)

    for a in articles:
        slug = slugify(a["title"])
        md = clean_markdown(to_markdown(a["body"]))
        h = content_hash(md)

        new_state[slug] = h
        file_path = OUTPUT / f"{slug}.md"

        if old_state.get(slug) == h:
            skipped += 1
            continue

        # NEW or UPDATED → write file
        file_path.write_text(f"# {a['title']}\n\n{md}", encoding="utf-8")
        changed_files.append(file_path)

        if slug in old_state:
            updated += 1
            log(f"Updated: {slug}")
        else:
            added += 1
            log(f"Added: {slug}")

    uploaded = upload_changed_files(changed_files)
    save_state(new_state)

    log(
        f"Job finished | added={added}, updated={updated}, skipped={skipped}, uploaded={uploaded}"
    )
    log("=== Exit 0 ===")

if __name__ == "__main__":
    main()
