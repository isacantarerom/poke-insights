# 🧠 PokéInsights — Distributed Backend Learning Project

> A two-service backend system built to practice real-world distributed architecture patterns: message queues, async communication, REST APIs, polyglot services, and containerized deployment.

---

## 📌 Project Summary

**PokéInsights** is a learning-focused backend project where two independent services communicate asynchronously via a message queue. It uses the free [PokéAPI](https://pokeapi.co/) as an external data source so we can focus on architecture, not auth tokens.

This is **not a tutorial you follow passively** — it's a project you build step by step, with each phase introducing a new concept.

---

## 🏗️ Architecture Overview

```
[Client / curl / Postman]
         │
         ▼
  ┌─────────────────┐        ┌───────────────────┐        ┌─────────────────┐
  │   Service A     │        │   Message Queue   │        │   Service B     │
  │  "The Collector"│──────▶│    (RabbitMQ)     │──────▶│  "The Analyst"  │
  │  Python/FastAPI │        │                   │        │  TypeScript /   │
  │   Port: 8000    │        │                   │        │  Express        │
  └─────────────────┘        └───────────────────┘        │   Port: 8001    │
         │                                                 └─────────────────┘
         ▼                                                          │
  PokéAPI (external)                                                ▼
  https://pokeapi.co                                       PostgreSQL / SQLite
```

### Service A — "The Collector" (Python + FastAPI)
- Receives requests to collect Pokémon data
- Calls the external PokéAPI
- Calculates a simple **battle power score** from base stats
- Publishes enriched data as a message onto RabbitMQ
- Exposes: `POST /collect?pokemon={name}` and `GET /health`

### Service B — "The Analyst" (TypeScript + Express)
- Subscribes to RabbitMQ and **consumes** incoming messages
- Persists Pokémon records to a database
- Exposes query endpoints for downstream consumers
- Exposes: `GET /pokemon/:name`, `GET /leaderboard`, `GET /health`

---

## 🧰 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Service A language | Python 3.11+ | Industry standard for data ingestion & pipelines |
| Service B language | TypeScript (Node.js) | Dominant in backend APIs; polyglot practice |
| API Framework A | FastAPI | Modern, async-native, auto-docs |
| API Framework B | Express.js | Lightweight, ubiquitous in real codebases |
| Message Queue | RabbitMQ | Real-world standard; teaches pub/sub and consumer patterns |
| Database | PostgreSQL (or SQLite to start) | Relational, widely used |
| Containerization | Docker + docker-compose | Run everything with one command |
| External API | [PokéAPI](https://pokeapi.co/) | Free, no auth, rich data |

---

## 📁 Repo Structure

```
pokeinsights/
├── docker-compose.yml          # Spins up everything together
├── README.md                   # This file
│
├── service-a-collector/        # Python / FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app entry point
│   ├── collector.py            # PokéAPI fetching logic
│   ├── publisher.py            # RabbitMQ publishing logic
│   └── models.py               # Data models / schemas
│
└── service-b-analyst/          # TypeScript / Express
    ├── Dockerfile
    ├── package.json
    ├── tsconfig.json
    ├── src/
    │   ├── index.ts            # Express app entry point
    │   ├── consumer.ts         # RabbitMQ consumer logic
    │   ├── db.ts               # Database connection & queries
    │   ├── routes.ts           # API route handlers
    │   └── models.ts           # TypeScript interfaces / types
    └── ...
```

---

## 🚀 Build Phases (Learning Roadmap)

Each phase introduces a new architectural concept. Build them in order.

### ✅ Phase 1 — Project setup & Docker
**Goal:** Get both services running in containers, communicating with nothing yet.
[x] Set up folder structure and git repo
[x] Create virtual environment
[x] Add virtual enviornment to the .gitignore
[x] Implement `GET /health` endpoint


**Key concepts:** Docker basics, docker-compose networking, service discovery by hostname

---

### ✅ Phase 2 — Service A Fetches from PokéAPI
**Goal:** Service A can call an external API and return structured data.
[x] Implement `POST /collect?pokemon=name`
[x] Call PokéAPI and extract: name, types, base stats (hp, attack, defense, speed)
[x] Calculate a simple `battle_power = (attack + defense + speed) * (hp / 100)`
[x] Return enriched JSON response

**Key concepts:** HTTP clients (`httpx` in Python), async/await, Pydantic models, error handling for 404s

---

### ✅ Phase 3 — Service A Publishes to RabbitMQ
**Goal:** After fetching data, push it onto a queue instead of just returning it.
[x] Add RabbitMQ connection using `pika` library
[x] After enriching data, publish a JSON message to a queue named `pokemon.collected`

**Key concepts:** Message queues, producer pattern, connection pooling, message serialization

---

### ✅ Phase 4 — Service B Consumes from RabbitMQ
**Goal:** Service B wakes up, reads the message, and stores it.
[x] Set up `amqplib` in TypeScript
[x] Write a consumer that listens to `pokemon.collected`

**Key concepts:** Consumer pattern, message acknowledgement, at-least-once delivery

---

### ✅ Phase 5 — Service B Exposes Query Endpoints
**Goal:** Clients can query processed Pokémon data.
- `GET /health` — basic health check
- `GET /pokemon/:name` — return stored stats for a Pokémon
- `GET /leaderboard` — top 10 Pokémon by `battle_power`, sorted descending
- Add basic input validation

**Key concepts:** REST design, query patterns, response shaping

---

### ✅ Phase 6 — Resilience & Error Handling
**Goal:** The system handles failures gracefully, like a production system would.
- Service A: retry PokéAPI calls on transient failures (exponential backoff)
- Service A: return clear errors for unknown Pokémon names
- Service B: don't crash if the DB is temporarily unavailable
- Service B: log failed messages before sending to dead-letter queue
- Add basic structured logging to both services

**Key concepts:** Retry patterns, dead-letter queues, structured logging, graceful degradation

---

### ✅ Phase 7 — Polish & GitHub Cleanup
**Goal:** The repo is clean, readable, and presentable on GitHub.
- Add a Postman collection (or `.http` file) to test all endpoints
- Add `.env.example` files for all environment variables
- Write clear commit history
- Update this README with any final changes
- Add a `LEARNINGS.md` file documenting what you discovered

---

## 🔌 API Reference

### Service A — Collector (Port 8000)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check — returns `{ status: "ok" }` |
| POST | `/collect?pokemon={name}` | Fetches Pokémon, enriches, publishes to queue |

**Example response from `/collect?pokemon=charizard`:**
```json
{
  "name": "charizard",
  "types": ["fire", "flying"],
  "stats": {
    "hp": 78,
    "attack": 84,
    "defense": 78,
    "speed": 100
  },
  "battle_power": 204.96,
  "published_at": "2025-01-01T12:00:00Z"
}
```

---

### Service B — Analyst (Port 8001)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/pokemon/:name` | Returns stored stats for a Pokémon |
| GET | `/leaderboard` | Top 10 Pokémon by battle_power |

**Example response from `/leaderboard`:**
```json
[
  { "name": "mewtwo", "battle_power": 312.5, "types": ["psychic"] },
  { "name": "charizard", "battle_power": 204.96, "types": ["fire", "flying"] }
]
```

---

## ⚙️ Running the Project

### Prerequisites
- Docker + Docker Compose installed
- Git

### Start Everything
```bash
git clone https://github.com/YOUR_USERNAME/poke-insights.git
cd pokeinsights
docker-compose up --build
```

### Verify Services
```bash
# Check Service A
curl http://localhost:8000/health

# Check Service B  
curl http://localhost:8001/health

# Collect a Pokémon (triggers the whole pipeline)
curl -X POST "http://localhost:8000/collect?pokemon=pikachu"

# Query the results (after a moment)
curl http://localhost:8001/pokemon/pikachu
curl http://localhost:8001/leaderboard

# RabbitMQ Management UI
open http://localhost:15672
# Login: guest / guest
```

---

## 🌍 Environment Variables

### Service A (`.env`)
```
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
LOG_LEVEL=INFO
```

### Service B (`.env`)
```
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
DATABASE_URL=postgresql://postgres:postgres@db:5432/pokeinsights
LOG_LEVEL=info
```

---

## 📚 Learning Concepts Index

If you want to review a concept after building it, here's where it appears:

| Concept | Phase | Service |
|---|---|---|
| REST API design | 2, 5 | A + B |
| External API integration | 2 | A |
| Pydantic / data validation | 2 | A |
| Async HTTP clients | 2 | A |
| Message queue (producer) | 3 | A |
| Message queue (consumer) | 4 | B |
| Message acknowledgement | 4 | B |
| Dead-letter queues | 4, 6 | B |
| Database persistence | 4, 5 | B |
| Retry + backoff patterns | 6 | A |
| Structured logging | 6 | A + B |
| Docker + docker-compose | 1 | Both |
| Polyglot services | Throughout | Both |
| Health checks | 2, 5 | A + B |

---

## 🧠 LEARNINGS.md

> TBD
---

## 🗂️ Resources

- [PokéAPI Docs](https://pokeapi.co/docs/v2)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [amqplib (Node)](https://github.com/amqp-node/amqplib)
- [pika (Python)](https://pika.readthedocs.io/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)

---

*Built as a learning project to practice distributed systems, message queues, and polyglot backend architecture.*