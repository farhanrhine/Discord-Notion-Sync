import os
import re
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()


def _get_notion_client_and_page_id():
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_page_id = os.getenv("NOTION_PAGE_ID")

    if not notion_api_key:
        raise ValueError("NOTION_API_KEY is missing in environment variables.")
    if not notion_page_id:
        raise ValueError("NOTION_PAGE_ID is missing in environment variables.")

    return Client(auth=notion_api_key), notion_page_id


def save_note(text):
    # Normalize model/user text so each Notion bullet is clean and single-line.
    cleaned_text = " ".join((text or "").split())
    cleaned_text = re.sub(r"^[-*•\s]+", "", cleaned_text)
    if not cleaned_text:
        raise ValueError("Note text is empty after cleanup.")

    notion, notion_page_id = _get_notion_client_and_page_id()
    notion.blocks.children.append(
        block_id=notion_page_id,
        children=[
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": cleaned_text,
                            },
                        }
                    ]
                },
            }
        ],
    )


def read_notes():
    notion, notion_page_id = _get_notion_client_and_page_id()
    response = notion.blocks.children.list(block_id=notion_page_id)

    notes = []
    for block in response["results"]:
        if block["type"] == "bulleted_list_item":
            rich_text = block["bulleted_list_item"].get("rich_text", [])
            if rich_text:
                notes.append(rich_text[0]["plain_text"])
        elif block["type"] == "child_page":
            title = block["child_page"].get("title")
            if title:
                notes.append(title)
        elif block["type"] == "paragraph":
            rich_text = block["paragraph"]["rich_text"]
            if rich_text:
                notes.append(rich_text[0]["plain_text"])

    if not notes:
        return "No notes found."

    bullet_lines = [f"- {note}" for note in notes]
    return "\n".join(bullet_lines)