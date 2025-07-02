# LLM + MCP + PostgreSQL + Chroma – Demo

Minimalny proof-of-concept pokazujący, jak:

1. uruchomić **FastAPI** w Dockerze,  
2. podłączyć **PostgreSQL** i **Chroma** przez **Model Context Protocol (MCP)**,  
3. pozwolić **GPT-4** wykonywać zapytania SQL i wyszukiwać wektorowo.

## 1 Wymagania

| narzędzie        | wersja |
|------------------|--------|
| Docker Desktop   | 20.10+ |
| Docker Compose V2| 2.x    |
| Klucz OpenAI     | dowolny|

> Windows 11: Docker wymaga włączonego WSL 2 oraz wirtualizacji w BIOS-ie.

## 2 Instalacja

```bash
git clone <repo-url> llm-mcp
cd llm-mcp
