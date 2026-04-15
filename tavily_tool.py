import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

load_dotenv()

WEB_SYSTEM_PROMPT = """You are a helpful assistant that answers using live web information.
Use the TavilySearch tool when you need recent or real-time information.
Answer concisely and directly.
IMPORTANT: Always include the source links/URLs in your response after each fact or section.
Format links like: [Link: https://example.com]
If the search results do not fully support the answer, say that clearly.
"""


def build_web_agent(model):
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY is missing in environment variables.")

    tavily_tool = TavilySearch(
        max_results=5,
        topic="general",
        include_answer="basic",
    )

    return create_agent(
        model=model,
        tools=[tavily_tool],
        system_prompt=WEB_SYSTEM_PROMPT,
    )


def _content_to_text(content):
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif "text" in item:
                    parts.append(str(item["text"]))
        return "".join(parts).strip()

    if content is None:
        return ""

    return str(content).strip()


def extract_agent_text(result):
    if not isinstance(result, dict):
        return _content_to_text(result)

    messages = result.get("messages", [])
    for message in reversed(messages):
        if getattr(message, "type", None) == "ai":
            return _content_to_text(getattr(message, "content", message))
        if isinstance(message, dict) and message.get("role") == "assistant":
            return _content_to_text(message.get("content"))

    if "structured_response" in result:
        return _content_to_text(result["structured_response"])

    return _content_to_text(result)
