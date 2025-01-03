from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import subprocess
import os
from uuid import uuid4
import shutil

app = FastAPI()

# Define a model for the input parameters
# class MMSeqsParams(BaseModel):
#     query: str  # The query sequence
#     database: str
#     output: str  # The output directory
#     sensitivity: float = 7.5  # Sensitivity parameter for mmseqs2
#     threads: int = 4  # Number of threads to use
#     blast_format: bool = True  # Option to convert to BLAST+ format

# # Dictionary to keep track of running jobs and results
# job_results = {}

def create_fastas_file_from_seq(seq, filename):
    with open(filename, 'w') as file:
        file.write(f">seq\n{seq}\n")

def create_queryDB_from_seq(filename):
    # this will create a db from a single sequence file
    # the command is mmseqs createdb <input> <output>
    # the output should be a file with the same name as the input but with the extension .db

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
            ["mmseqs", "--help"],
            capture_output=True,
            text=True,
        )
        return {"help": results.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Command failed {e.stderr}")

@app.post("/run_mmseqs")
async def run_mmseqs(request: Request):
    
    data = await request.json()
    
    print(f" Received request to run blastp with data: {data}"))
    
    query_filename =f"in.fasta"
    result_filename = f"out.out"
    
    # Clear or create result file 
    open(result_filename, 'w').close()
    
    # Create the fasta file from the query string
    create_fastas_file_from_seq(data['query'], query_filename)
    # Create a unique job id
    # job_id = str(uuid4())
    # output_dir = f"/tmp/{job_id}"

    # # Prepare the output directory
    # os.makedirs(output_dir, exist_ok=True)

    # # Prepare paths
    # result_m8_path = os.path.join(output_dir, "result.m8")
    # result_tsv_path = os.path.join(output_dir, "result.tsv")

    # # Create the FASTA file
    # path_query = os.path.join(output_dir, "query.fasta")
    # path_queryDB = path_query.replace('fasta', '') + ".db"
    # create_fastas_file_from_seq(params.query, path_query)
    # create_queryDB_from_seq(path_query)

    # Run the mmseqs2 search command
    command = [
        "mmseqs", "search", 
        query_filename, 
        data['db'], 
        result_filename,
        "--threads", str(data['threads']), 
        "--sensitivity", str(data['sensitivity'])
    ]

    try:
        # Execute mmseqs search
        subprocess.run(command, check=True)

        # Convert the results to BLAST+ format if requested
        if data['blast_format']:
            # mmseqs convertalis queryDB targetDB resultDB resultDB.m8
            # Convert to BLAST tabular format (BLAST m8 format)
            convert_command = [
                "mmseqs", "convertalis", 
                data['query'], 
                data['database'], 
                result_filename, 
            ]
            subprocess.run(convert_command, check=True)
            
            # Store the result path for m8 format
            job_results[job_id] = {
                "status": "completed",
                "result_path": result_m8_path
            }
        else:
            # Store the result path for standard mmseqs2 output (TSV format)
            job_results[job_id] = {
                "status": "completed",
                "result_path": result_tsv_path
            }

        return {"job_id": job_id}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"mmseqs2 failed: {str(e)}")

@app.get("/results/{job_id}")
async def get_results(job_id: str):
    # Check if the job exists
    if job_id not in job_results:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get the result path
    result = job_results[job_id]

    # Read and return the result (assuming it's a text file you want to read and return)
    result_file = result["result_path"]
    if os.path.exists(result_file):
        with open(result_file, "r") as file:
            data = file.read()
        return {"status": result["status"], "results": data}
    else:
        raise HTTPException(status_code=404, detail="Result file not found")


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)