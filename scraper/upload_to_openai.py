import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=BASE_DIR / "backend" / ".env")
print("VECTOR_STORE_ID:", os.getenv("VECTOR_STORE_ID"))

client = OpenAI()

ARTICLES_DIR = Path("output/articles")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")


def create_vector_store():
    vs = client.vector_stores.create(
        name="optisigns-support-docs"
    )
    print("Vector store created:", vs.id)
    return vs.id


def upload_and_embed():
    paths = list(ARTICLES_DIR.glob("*.md"))

    batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=VECTOR_STORE_ID,
        files=paths
    )

    print("Files embedded:", batch.file_counts.completed)
    print("Chunks embedded:", batch.file_counts.total)
    return batch.file_counts.completed


def attach_vector_store_to_assistant():
    client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [VECTOR_STORE_ID]
            }
        }
    )
    print("Vector store attached to assistant")


def upload_changed_files(paths):
    if not paths:
        return 0

    if not VECTOR_STORE_ID:
        raise RuntimeError("VECTOR_STORE_ID not set")

    batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=VECTOR_STORE_ID,
        files=[open(p, "rb") for p in paths]
    )

    return batch.file_counts.completed


if __name__ == "__main__":
    upload_and_embed()
    attach_vector_store_to_assistant()
