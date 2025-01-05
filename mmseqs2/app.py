from fastapi import FastAPI, HTTPException, Request
import logging

import subprocess
import os

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("FastAPI server is running...")


def create_fastas_file_from_seq(queries, filename):
    with open(filename, 'w') as f:
        for idx, query in enumerate(queries):
            f.write(f">seq{idx}\n{query}\n")
    print(f"FASTA file created: {filename}")

def create_queryDB_from_seq(filename):

    command = [
        "mmseqs", "createdb",
        filename,
        filename.replace('fasta', '') + ".db"
    ]

    try:
        subprocess.run(command, check=True)
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=600, detail=str(e))
    

@app.get("/")
async def read_root():
    return {"message": "Welcome to the MMSeqs2 API!"}

@app.get("/help")
def help():
    try: 
        results = subprocess.run(
            ["mmseqs", "-h"],
            capture_output=True,
            text=True,
        )
        return {"help": results.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Command failed {e.stderr}")


@app.post("/easycluster")
async def easycluster(request: Request):
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    data = await request.json()
    logger.info(f"Received request data: {data}")
    
    print(f" Received request to run mmseqs with data: {data}")
    
    query_filename =f"in.fasta"
    result_filename = f"out.out"
    
    # Clear or create result file 
    open(result_filename, 'w').close()
    
    # Create the fasta file from the query string
    create_fastas_file_from_seq(data['query'], query_filename)

    # Run the mmseqs2 search command
    # command = [
    #     "mmseqs", "easy-cluster", 
    #     query_filename, 
    #     result_filename,
    #     "--min-seq-id", request['min_seq_id'], 
    #     "-c", request['coverage'], 
    #     "--cov-mode", request['cov_mode'],
    #     "tmp"
    # ]
    command = [
        "mmseqs", "easy-cluster", 
        query_filename, 
        result_filename,
        "--min-seq-id", str(data['min_seq_id']), 
        "-c", str(data['coverage']), 
        "--cov-mode", str(data['cov_mode']),
        "tmp"
    ]
    logger.info(f"Running command: {' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"MMSeqs command failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    with open(result_filename, 'r') as file:
        result = file.read()

    return result


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)