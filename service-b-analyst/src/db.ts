import initSqlJs, { Database } from 'sql.js'
import * as fs from 'fs'

const DB_PATH = 'pokeinsights.db.json'
let db: Database

export async function initDb() {
  const SQL = await initSqlJs()
  db = new SQL.Database()
  db.run(`
    CREATE TABLE IF NOT EXISTS pokemon (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE,
      types TEXT,
      hp INTEGER,
      attack INTEGER,
      defense INTEGER,
      special_attack INTEGER,
      special_defense INTEGER,
      speed INTEGER,
      battle_power REAL,
      collected_at TEXT
    )
  `)
  console.log('Database ready')
}

export function savePokemon(data: any) {
  db.run(`
    INSERT OR REPLACE INTO pokemon 
    (name, types, hp, attack, defense, special_attack, special_defense, speed, battle_power, collected_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `, [
    data.name,
    JSON.stringify(data.types),
    data.stats.hp,
    data.stats.attack,
    data.stats.defense,
    data.stats.special_attack,
    data.stats.special_defense,
    data.stats.speed,
    data.battle_power,
    new Date().toISOString()
  ])
}

export function getPokemon(name: string) {
  const result = db.exec('SELECT * FROM pokemon WHERE name = ?', [name])
  if (!result.length) return null
  const cols = result[0].columns
  const row = result[0].values[0]
  return Object.fromEntries(cols.map((c, i) => [c, row[i]]))
}

export function getLeaderboard() {
  const result = db.exec('SELECT * FROM pokemon ORDER BY battle_power DESC LIMIT 10')
  if (!result.length) return []
  const cols = result[0].columns
  return result[0].values.map(row => Object.fromEntries(cols.map((c, i) => [c, row[i]])))
}