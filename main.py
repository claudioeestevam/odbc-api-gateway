from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
import os

app = FastAPI()

class QueryRequest(BaseModel):
    sql: str

def get_connection():
    dsn = os.getenv("ODBC_DSN")
    user = os.getenv("ODBC_USER")
    password = os.getenv("ODBC_PASSWORD")
    conn_str = f"DSN={dsn};UID={user};PWD={password};TrustServerCertificate=yes"
    return pyodbc.connect(conn_str)

@app.get("/")
def root():
    return {
        "company": "LeverPro",
        "application": "ODBC-API-Gateway",
        "version": "1.0.0"
    }

@app.post("/query/")
def run_query(req: QueryRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(req.sql)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in result]
        return {"rows": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))