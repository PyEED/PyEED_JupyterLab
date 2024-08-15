from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import subprocess
import os
import uuid
from typing import Optional
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class BlastRequest(BaseModel):
    tool: str
    query: str
    db: str
    evalue: str
    outfmt: str


## ENDPOINTS --------------------------

def create_fastas_file_from_seq(seq, filename):
    with open(filename, 'w') as file:
        file.write(f">seq\n{seq}\n")

# this get json params
@app.post("/run_blast")
async def run_blast(request: Request):
    request = await request.json()

    query_filename = f"in.fasta"
    result_filename = f"out.out"
    # create empty file
    open(result_filename, 'w').close()

    # Create the FASTA file
    create_fastas_file_from_seq(request['query'], query_filename)

    # Run the BLAST command
    command = [
        request['tool'],
        '-query', query_filename,
        '-db', request['db'],
        '-evalue', request['evalue'],
        '-outfmt', request['outfmt'],
        '-num_threads', request['num_threads'],
        '-out', result_filename
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))


    with open(result_filename, 'r') as file:
        result = file.read()

    return result



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=6001, reload=True)
