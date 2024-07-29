from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import subprocess
import os
import uuid
from typing import Optional

app = FastAPI()

## IN AND OUT DATA MODELS -------------

class BlastRequest(BaseModel):
    tool: str
    query: str
    db: str
    evalue: Optional[str] = '0.001'
    outfmt: Optional[str] = '6'

## ENDPOINTS --------------------------

@app.post("/run_blast", response_model=dict)
async def run_blast(request: BlastRequest):
    query_filename = f"/app/data/{uuid.uuid4()}.fasta"
    result_filename = f"/app/data/{uuid.uuid4()}.out"

    # Save the query to a file
    with open(query_filename, 'w') as query_file:
        query_file.write(request.query)

    # Run the BLAST command
    command = [
        request.tool,
        '-query', query_filename,
        '-db', request.db,
        '-evalue', request.evalue,
        '-outfmt', request.outfmt,
        '-out', result_filename
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))


    with open(result_filename, 'r') as file:
        result = file.read()

    return {"result": result}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=6001, reload=True)
