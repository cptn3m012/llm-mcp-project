# LLM MCP Project

A simple demo project showing how an LLM agent can interact with a PostgreSQL database through an MCP-style server.

The application uses **FastAPI**, **LangChain**, **OpenAI**, **PostgreSQL**, and **Docker Compose**.

---

## Features

- Natural language questions handled by an LLM agent
- PostgreSQL database integration
- MCP-style server for database access
- Read-only SQL execution
- FastAPI backend
- Docker Compose setup
- Simple CLI client
- Adminer for database preview

---

## Tech Stack

- Python 3.11
- FastAPI
- LangChain
- OpenAI API
- PostgreSQL
- Docker
- Docker Compose
- Adminer

---

## Project Structure

```text
llm-mcp-project/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init/
├── mcp-servers/
│   └── postgres/
├── scripts/
│   └── ask.py
├── docker-compose.yml
└── README.md
```

---

## Requirements

Before running the project, make sure you have installed:

- Docker
- Docker Compose
- Python 3.11+
- OpenAI API key

---

## Environment Variables

Create a `.env` file inside the `backend` folder:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/cptn3m012/llm-mcp-project.git
cd llm-mcp-project
```

Start the application:

```bash
docker-compose up --build -d
```

Check if containers are running:

```bash
docker-compose ps
```

---

## API

### Health Check

```http
GET /health
```

Example:

```bash
curl http://localhost:8000/health
```

---

### Ask a Question

```http
POST /query
```

Example:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How many users are in the database?"}'
```

---

## CLI Client

Run the CLI client:

```bash
python scripts/ask.py
```

Example questions:

```text
How many users are in the database?
Show me all posts.
Which user has the most posts?
```

To exit:

```text
exit
```

---

## Adminer

Adminer is available at:

```text
http://localhost:8080
```

Database login:

```text
System: PostgreSQL
Server: pg
Username: llm_user
Password: llm_pass
Database: llm_db
```

---

## Database

PostgreSQL is available locally on:

```text
localhost:5433
```

Default credentials:

```text
Database: llm_db
User: llm_user
Password: llm_pass
```

---

## Stop the Application

Stop containers:

```bash
docker-compose down
```

Stop containers and remove database volume:

```bash
docker-compose down -v
```

---

## Notes

This project is a proof of concept.

The database tool is designed for read-only SQL queries.

For production use, add proper authentication, stronger SQL validation, logging, rate limiting, and secure secret management.

## License

This project is licensed under the MIT License.
