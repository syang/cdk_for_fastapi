from fastapi import FastAPI


app = FastAPI()

# Using this endpoint for health check
@app.get("/")
def read_root():
    return "Hello World"
