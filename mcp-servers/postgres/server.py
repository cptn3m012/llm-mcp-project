from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, psycopg2, json
from psycopg2.extras import RealDictCursor

DB_DSN = os.getenv("MCP_POSTGRES_DSN")
app = FastAPI(title="MCP-Postgres Server")


def get_db_schema():
    """
    Connects to the database and generates the schema in CREATE TABLE format
    based on metadata from information_schema.
    """
    schema_parts = []
    with psycopg2.connect(DB_DSN) as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 1. Get all tables in the 'public' schema
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        tables = cur.fetchall()

        # 2. For each table, get its column definitions
        for table in tables:
            table_name = table['table_name']
            cur.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            columns = cur.fetchall()

            # 3. Build the 'CREATE TABLE' fragment for the current table
            columns_defs = []
            for col in columns:
                col_def = f"  {col['column_name']} {col['data_type']}"
                if col['is_nullable'] == 'NO':
                    col_def += " NOT NULL"
                columns_defs.append(col_def)

            # Add the complete table definition to list
            schema_parts.append(f"CREATE TABLE {table_name} (\n" + ",\n".join(columns_defs) + "\n);")

    # Return the combined definitions of all tables
    return "\n\n".join(schema_parts)


@app.get("/schema")
def get_schema_endpoint():
    """Endpoint that returns the current database schema in text format."""
    try:
        schema = get_db_schema()
        return {"schema": schema}
    except Exception as e:
        # In case of a connection or query problem, return a server error.
        raise HTTPException(status_code=500, detail=f"Error generating schema: {e}")


class CallBody(BaseModel):
    name: str
    arguments: dict


@app.get("/tools/list")
def list_tools():
    """Returns the list of available tools."""
    return [{
        "name": "query",
        "description": "Execute read-only SQL (SELECT) on Postgres",
        "parameters": {
            "type": "object",
            "properties": {"sql": {"type": "string"}},
            "required": ["sql"]
        }
    }]


@app.post("/tools/call")
def call_tool(body: CallBody):
    """Executes an SQL query"""
    if body.name != "query":
        raise HTTPException(400, "unknown tool")

    sql = body.arguments.get("sql")
    if not sql:
        raise HTTPException(400, "Missing 'sql' argument")

    print(f"DEBUG: Received SQL query: {sql}")
    if not sql.lstrip().lower().startswith("select"):
        raise HTTPException(400, "Only SELECT queries are allowed")

    try:
        with psycopg2.connect(DB_DSN) as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        return {"ok": True, "result": json.dumps(rows, default=str)}
    except psycopg2.Error as e:
        print(f"SQL EXECUTION ERROR: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Error executing SQL query: {e}"
        )
