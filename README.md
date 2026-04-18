# Discord-Notion-Sync

An intelligent Discord bot that serves as a bridge between your chat and your Notion workspace.

> "You don't always need a complex UI to build a powerful AI agent. By combining Discord for the interface, LangChain for the logic, and Tavily for web search, you can turn a boring bot into a natural language assistant that provides real-time chat and saves your notes to Notion."

## 🚀 Features

- **AI-Powered Note Saving**: Save raw text or use AI to refine and summarize notes directly into Notion.
- **Web Search Agent**: Integrated Tavily-powered search agent to answer complex queries with live web data.
- **Notion Integration**: Read and write notes to your Notion database seamlessly.
- **LLM Support**: Powered by Groq (Qwen) for fast, high-quality reasoning.

## 🏗️ Architecture & Workflow

```mermaid
flowchart TD
    %% Define Styles
    classDef user fill:#FFB74D,stroke:#F57C00,stroke-width:2px,color:#000;
    classDef discord fill:#5865F2,stroke:#fff,stroke-width:2px,color:#fff;
    classDef bot fill:#2C2F33,stroke:#7289DA,stroke-width:2px,color:#fff;
    classDef agent fill:#66BB6A,stroke:#388E3C,stroke-width:2px,color:#fff;
    classDef notion fill:#ECEFF1,stroke:#CFD8DC,stroke-width:2px,color:#000;
    classDef tavily fill:#FF7043,stroke:#E64A19,stroke-width:2px,color:#fff;
    classDef LLM fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff;

    User([User]):::user -->|Message| Discord[Discord Channel]:::discord
    Discord -->|Events/Commands| Bot{bot.py Router}:::bot

    %% Command Routing Logic
    Bot -->|!note save| NotionNode[notion.py \n Raw Save / Read]:::notion
    Bot -->|!note save ai| LLM[LLM \n Refine Text]:::LLM
    Bot -->|!note read| NotionNode
    Bot -->|!search| AgentNode[tavily_tool.py \n Web Search]:::agent
    Bot -->|!<anything else>| LLM[LLM \n Chat]:::LLM

    %% Data Flow & External Connections
    LLM -->|Passes Refined Note| NotionNode
    NotionNode <-->|API| NotionDB[(Notion Database)]:::notion
    AgentNode <-->|Queries| Tavily[Tavily Search API]:::tavily
    AgentNode <-->|Reasons| LLM
```

## 📁 Project Structure

```text
├── bot.py           # Main Discord bot and command routing
├── notion.py        # Notion API integration (save/read notes)
├── tavily_tool.py   # LangChain agent powered by Tavily for web search
├── pyproject.toml   # Project dependencies and configurations
└── .env             # API keys and tokens (Discord, Notion, Groq, Tavily)
```



## 📋 Prerequisites

Before you begin, ensure you have:
- [uv](https://github.com/astral-sh/uv) installed on your system.
- A **Discord Developer Application** with a generated Bot Token.
- A **Notion Integration** token and a target Page/Database ID.
- API keys from **Groq** and **Tavily**.

## 🛠️ Setup

1. Copy `.env.example` to `.env` and fill in your credentials:
   - `DISCORD_TOKEN`
   - `NOTION_TOKEN`
   - `NOTION_PAGE_ID`
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Run the bot:
   ```bash
   uv run bot.py
   ```

## ⌨️ Commands

- `!note save <text>`: Save a raw note to Notion.
- `!note save ai <text>`: Refine text with AI and save it.
- `!note read`: Fetch recent notes from Notion.
- `!search <query>`: Ask the web agent to research something.
- `!<anything else>`: Acts as a general chat with the LLM (e.g., `!hello`).
