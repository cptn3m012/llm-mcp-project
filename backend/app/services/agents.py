import os
from typing import Any, Optional

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool, tool
from langchain_openai import ChatOpenAI

import app.mcp_client as mcp

# --------------------------------------------------------------------------
# Model Configuration
# --------------------------------------------------------------------------
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")
_llm = ChatOpenAI(
    model_name=MODEL_NAME,
    temperature=0,
    max_retries=5,
    timeout=60,
)

# --------------------------------------------------------------------------
# Global state variables
# --------------------------------------------------------------------------
_agent: Optional[Any] = None
_schema: Optional[str] = None


# --------------------------------------------------------------------------
# Tool generation from MCP metadata
# --------------------------------------------------------------------------
def _make_tool(meta: dict) -> Tool:
    srv = meta["__server"]
    name = meta["name"]
    desc = meta.get("description", f"{name} tool on {srv}")

    def _run(tool_input: Any = None, **kwargs):
        if tool_input is not None:
            if isinstance(tool_input, dict):
                kwargs = tool_input
            else:
                kwargs = {"sql": str(tool_input)}

        # --- DODANA LINIA DO LOGOWANIA ---
        print(
            f"--- AGENT IS EXECUTING TOOL 'query' WITH SQL ---\n{kwargs.get('sql')}\n-------------------------------------------------")
        # ------------------------------------

        return mcp.call(srv, name, kwargs)

    return Tool(name=name, description=desc, func=_run)


# --------------------------------------------------------------------------
# Simple chat tool
# --------------------------------------------------------------------------
@tool
def chat(message: str) -> str:
    """A simple echo - responds with the same text."""
    return message


def initialize_global_agent_and_schema():
    """
    Initializes the global agent and schema right at application startup.
    This function is called only once when the module is imported.
    """
    global _agent, _schema

    if _agent is not None:
        return

    print("Startup initialization: Fetching database schema...")
    _schema = mcp.get_schema()
    print("--- FETCHED SCHEMA ---")
    print(_schema)
    print("----------------------")

    tools_meta = mcp.all_tools()
    tools = [chat] + [_make_tool(m) for m in tools_meta]
    if not tools:
        raise RuntimeError("No MCP tools available - agent cannot be initialized.")

    _agent = initialize_agent(
        tools=tools,
        llm=_llm,
        agent=AgentType.OPENAI_MULTI_FUNCTIONS,
    )
    print("Agent has been successfully initialized and is ready to work.")


initialize_global_agent_and_schema()


# --------------------------------------------------------------------------
# Agent invocation function
# --------------------------------------------------------------------------
def query_agent(prompt: str) -> str:
    """
    Prepares the prompt and calls the LangChain agent.
    It assumes that the agent and schema are already initialized.
    """
    if _agent is None or _schema is None:
        raise RuntimeError("Agent was not correctly initialized at application startup.")

    prompt_template = f"""
Based on the PostgreSQL database schema below, answer the user's question.
Your task is to generate a correct SELECT SQL query that will answer the question.
Use only the tables and columns defined in the schema below. Do not guess names.

[DATABASE SCHEMA]
{_schema}

[USER QUESTION]
{prompt}
"""

    print("--- FINAL PROMPT SENT TO LLM ---")
    print(prompt_template)
    print("------------------------------------")

    return _agent.run(prompt_template)
