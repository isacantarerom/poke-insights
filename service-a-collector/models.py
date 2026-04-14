from pydantic import BaseModel
from typing import List

class PokemonStats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

class PokemonResponse(BaseModel):
    name: str
    stats: PokemonStats
    types: List[str]
    battle_power: float