import httpx
import asyncio
from models import PokemonStats, PokemonResponse

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

async def fetch_pokemon(name: str) -> PokemonResponse:
    max_retries = 3
    wait_seconds = 1

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{POKEAPI_BASE_URL}{name.lower()}")

                if(response.status_code == 404):
                    return None

                response.raise_for_status()
                data = response.json()
                
                stats_map = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                types = [t['type']['name'] for t in data['types']]
                
                stats = PokemonStats(
                    hp=stats_map.get('hp', 0),
                    attack=stats_map.get('attack', 0),
                    defense=stats_map.get('defense', 0),
                    special_attack=stats_map.get('special-attack', 0),
                    special_defense=stats_map.get('special-defense', 0),
                    speed=stats_map.get('speed', 0)
                )

                battle_power = (stats.attack + stats.special_attack + stats.defense + stats.speed) * (stats.hp / 100)
                
                return PokemonResponse(
                    name=data['name'],
                    stats=stats,
                    types=types,
                    battle_power=round(battle_power, 2)
                )
        except httpx.HTTPStatusError as e:
            print(f"[ATTEMPT: {attempt + 1}] HTTP ERROR: {e}")
        except httpx.RequestError as e:
            print(f"[ATTEMPT {attempt +1}] NETWORK ERROR: {e}")
         
        if attempt < max_retries-1 :
            print(f"Retrying in {wait_seconds}s...")
            await asyncio.sleep(wait_seconds)
            wait_seconds*=2

    raise Exception(f"Failed to fetch '{name}' after {max_retries} attempts")