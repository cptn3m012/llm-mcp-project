import os
import time
import requests
from typing import Any, Dict, List

SERVERS = {
    "postgres": os.getenv("MCP_POSTGRES_URL", "http://mcp_postgres:3330"),
}


def get_schema(server: str = "postgres", retries: int = 10, delay: float = 2.0) -> str:
    """Fetches the database schema from the MCP server using the new /schema endpoint."""
    url = f"{SERVERS[server]}/schema"
    print(f"Sending schema request to: {url}")
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            return resp.json()["schema"]
        except requests.RequestException as e:
            print(f"Error fetching schema (attempt {attempt}/{retries}): {e}")
            if attempt == retries:
                raise
            time.sleep(delay)
    raise RuntimeError("Failed to fetch the database schema after multiple attempts.")


def _tools_of(server: str, retries: int = 10, delay: float = 2.0) -> List[Dict[str, Any]]:
    """Fetches the list of tools (no changes)."""
    url = f"{SERVERS[server]}/tools/list"
    for attempt in range(1, retries + 1):
        try:
            return requests.get(url, timeout=5).json()
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(delay)
    raise RuntimeError(f"Failed to fetch tools from server {server}.")


def all_tools() -> List[Dict[str, Any]]:
    """Gathers tools from all servers (no changes)."""
    out: List[Dict[str, Any]] = []
    for name in SERVERS:
        for t in _tools_of(name):
            t["__server"] = name
            out.append(t)
    return out


def call(server: str, tool: str, args: Dict[str, Any]) -> Any:
    """Calls a tool on the MCP server (no changes)."""
    url = f"{SERVERS[server]}/tools/call"
    payload = {
        "name": tool,
        "arguments": args,
    }
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
