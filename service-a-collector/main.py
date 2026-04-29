from fastapi import FastAPI, HTTPException
from collector import fetch_pokemon
from publisher import publish_pokemon
import logging

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/collect")
async def collect_pokemon(pokemon:str):
    logger.info(f"Collecting pokemon: {pokemon}")
    result = await fetch_pokemon(pokemon)

    if result is None:
        logger.warning(f"Pokemon not found: {pokemon}")
        raise HTTPException(status_code=404, detail=f"Pokemon '{pokemon}' not found")
    
    publish_pokemon(result.model_dump())
    logger.info(f"Published to queue: {pokemon} | battle_power: {result.battle_power}")
    
    return result