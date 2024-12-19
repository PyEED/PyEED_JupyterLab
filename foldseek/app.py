import os 
import subprocess

from fastapi import FastAPI, UploadFile, HTTPException, Request

app = FastAPI()

def create_fasta_files_from_seq(seq, filename):
    with open(filename, 'w') as file: 
        file.write(f">seq\n{seq}\n")


@app.get("/help_easy-search")
def foldseek_help(): 
    
    print("Received request for help")
    
    try: 
        results = subprocess.run(
            ["foldseek", "easy-search", "--help"],
            capture_output=True, 
            text=True,
        )
        return results.stdout
    
    except subprocess.CalledProcessError as e: 
        raise HTTPException(status_code=400, detail=f"Command failed: {e.stderr}")

@app.post("/easy-search")
async def easy_search(request: Request):
    
    data = await request.form()
    
    print(f" Received request to run blastp with data: {data}")
    
    query_filename = f"in.fasta"
    result_filename = f"out.out"
    
    # Clear or create result file
    open(result_filename, 'w').close()
    
    # Create the fasta file from the query string
    create_fasta_files_from_seq(data['query'], query_filename)
    
    try:
        command = [
            "foldseek",
            'easy-search', 
            '-e', str(data['evalue']),
            '-s', str(data['sensitivity']),
            '--format-output', str(data['format-output']),
            '-out', result_filename,
            '-max-seqs', str(data['maxseqs']), 
            '--cov-mode', str(data['cov-mode']),
            ]
        
        result = subprocess.run(
            command, 
            capture_output=True,
            check=True,
            text=True,
        )
        
        with open(result_filename, 'r') as file:
            result = file.read()
        
        return {"result": result}
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Command failed: {e.stderr}")
    
if __name__ == "__main__": 
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=7001, reload=True)