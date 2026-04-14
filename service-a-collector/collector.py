import httpx
from models import PokemonStats, PokemonResponse

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

async def fetch_pokemon(name: str) -> PokemonResponse:
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