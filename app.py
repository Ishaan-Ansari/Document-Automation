import uvicorn
from fastapi import FastAPI

# Tasks imports...

app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app!"}


# app.mount("/task_1", task_1_app)...

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)