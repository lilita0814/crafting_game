from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test/{msg}")
def read_item(msg: str = None):
    print(msg)
    return {}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=19132)
