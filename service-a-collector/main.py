from fastapi import FastAPI, HTTPException
from collector import fetch_pokemon
from publisher import publish_pokemon

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/collect")
async def collect_pokemon(pokemon:str):
    result = await fetch_pokemon(pokemon)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Pokemon '{pokemon}' not found")
    
    publish_pokemon(result.model_dump())
    
    return result