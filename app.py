from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def foo():
    return True

if __name__ == "__main__":
    uvicorn.run(app,port=8000)
