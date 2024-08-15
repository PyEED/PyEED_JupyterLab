from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from uuid import uuid4
import shutil

app = FastAPI()

# Define a model for the input parameters
class MMSeqsParams(BaseModel):
    query: str  # The query sequence
    database: str
    output: str  # The output directory
    sensitivity: float = 7.5  # Sensitivity parameter for mmseqs2
    threads: int = 4  # Number of threads to use
    blast_format: bool = True  # Option to convert to BLAST+ format

# Dictionary to keep track of running jobs and results
job_results = {}

@app.post("/run_mmseqs")
async def run_mmseqs(params: MMSeqsParams):
    # Create a unique job id
    job_id = str(uuid4())
    output_dir = f"/tmp/{job_id}"

    # Prepare the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Prepare paths
    result_m8_path = os.path.join(output_dir, "result.m8")
    result_tsv_path = os.path.join(output_dir, "result.tsv")

    # Run the mmseqs2 search command
    command = [
        "mmseqs", "search", 
        params.query, 
        params.database, 
        os.path.join(output_dir, "result"), 
        output_dir, 
        "--threads", str(params.threads), 
        "--sensitivity", str(params.sensitivity)
    ]

    try:
        # Execute mmseqs search
        subprocess.run(command, check=True)

        # Convert the results to BLAST+ format if requested
        if params.blast_format:
            # Convert to BLAST tabular format (BLAST m8 format)
            convert_command = [
                "mmseqs", "convertalis", 
                params.query, 
                params.database, 
                os.path.join(output_dir, "result"), 
                result_m8_path, 
                "--format-output", "query,target,evalue,raw,alnlen,identity,similarity"
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
    uvicorn.run("app:app", host="0.0.0.0", port=6001, reload=True)