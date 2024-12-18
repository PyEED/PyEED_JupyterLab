import os 
import subprocess

from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.get("/help")
def foldseek_help(): 
    print("Received request for help")
    try: 
        results = subprocess.run(
            ["foldseek", "--help"],
            capture_output=True, 
            text=True,
        )
        return results.stdout
    except subprocess.CalledProcessError as e: 
        return {"error": "Command failed", "stderr": e.stderr}, 400

@app.post("/easy-search")
def easy_search(file: UploadFile):
    path = f"/app/data/{file.filename}"
    with open (path, "wb") as f: 
        f.write(file.file.read())
        
    try:
        command = [
            "foldseek",
            "easy-search", 
            "-e", 
            "--max-seqs", 
            ]
    
if __name__ == "__main__": 
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=7001, reload=True)