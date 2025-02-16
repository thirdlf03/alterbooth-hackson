from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def read_root():
    return {"status": "UP"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)