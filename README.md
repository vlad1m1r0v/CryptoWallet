# CryptoWallet

A full-stack, event-driven cryptocurrency wallet & marketplace platform: manage Ethereum (Sepolia) wallets, send transactions, buy & sell products, and chat in real time.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.118-009688?logo=fastapi&logoColor=white)
![FastStream](https://img.shields.io/badge/FastStream-0.6-1B4F72?logo=rabbitmq&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte-5-FF3E00?logo=svelte&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Event--Driven%20Microservices-6A4C93)
![License](https://img.shields.io/badge/License-Unlicensed-lightgrey)

---

## About The Project

CryptoWallet is a full-stack application that merges a self-custody Ethereum wallet with a peer-to-peer marketplace and a real-time chat. It targets developers and enthusiasts who want a working reference implementation of how a modern fintech platform is engineered: users register, create or import ETH wallets, send crypto transactions, publish products, pay for orders on-chain, and chat — all updated live in the browser.

The main problem it solves is demonstrating how to build a secure, event-driven backend that keeps a SPA frontend synchronized in real time while dealing with asynchronous blockchain confirmations.

## Key Tech Stack

**Backend (Python 3.13)** — four decoupled services:

| Service | Path | Role | Key libraries |
| --- | --- | --- | --- |
| `rest_api` | `backend/rest_api` | REST API + event orchestration | FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Dishka, FastStream, TaskIQ, SlowAPI |
| `ethereum` | `backend/ethereum` | Blockchain integration | Web3.py, httpx, websockets, FastStream, Redis |
| `ibay` | `backend/ibay` | Marketplace order fulfillment | FastStream, SQLAlchemy 2.0, aiohttp |
| `sockets` | `backend/sockets` | Real-time push (Socket.IO) + chat | python-socketio, aiohttp, FastStream, PyMongo |

**Frontend** — `frontend/`: SvelteKit (Svelte 5) + TypeScript + Vite, `socket.io-client`, Felte + Zod forms, svelte-modals, svelte-sonner.

**Database & Caching:**
- PostgreSQL — relational core (users, wallets, assets, transactions, products, orders) with Alembic migrations
- MongoDB — chat messages & user profiles (via sockets service)
- Redis — pending-transaction registry (sorted set), Socket.IO message broker, TaskIQ queue + scheduler storage

**Broker / Tasks:**
- RabbitMQ — cross-service event bus (FastStream)
- TaskIQ workers + scheduler (Redis-backed) for background jobs

**DevOps / Deployment:**
- Docker multi-stage `Dockerfile`s for every backend service and the frontend
- Makefile-driven run commands (`server`, `worker`, `scheduler`, `faststream`, `socketio`)

## Core Features

- **Authentication & Profiles** — register/login with RS256 JWT, profile editing, avatar upload/delete to S3, password change
- **Ethereum Wallet Management** — create new wallets or import existing ones via private key; request free Sepolia ETH (rate-limited to 1/hour per user)
- **Transactions** — send ETH to any address; wallets and transactions are persisted; balances are tracked as `DECIMAL` wei
- **Blockchain Event Streaming** — Infura WebSocket block listener with a reconciliation loop for stuck transactions
- **Marketplace (iBay)** — create products with S3-hosted photos, place orders, on-chain payment, and a simulated fulfillment lifecycle (`NEW → DELIVERING → COMPLETED / RETURNED / FAILED`)
- **Real-Time Chat** — Socket.IO chat with presence, image/file upload, unread-message counters
- **Real-Time UI Sync** — wallet balance, pending/complete transactions, product and order updates pushed live to the browser
- **Security hardening** — bcrypt password hashing with an HMAC-SHA256 pepper, AES-256-CFB encryption of private keys at rest, rate limiting, CORS

## Architecture & Engineering Highlights

- **Hexagonal / Clean Architecture** (`rest_api`): strict separation of `domain` (entities, value objects, ports), `application` (interactors/use-cases), `infrastructure` (SQLAlchemy adapters, providers), and `presentation` (HTTP handlers, AMQP consumers).
- **Dependency Injection with Dishka** — an async DI container wires the whole graph (config, gateways, transaction managers, event publishers) across FastAPI, FastStream, and TaskIQ runtimes.
- **Event-Driven Choreography over RabbitMQ (FastStream)** — services never call each other directly. The REST API publishes domain events (`rest_api.create_transaction`, `rest_api.create_order`, ...); the `ethereum` service signs/broadcasts transactions and publishes `ethereum.create_pending_transaction` / `ethereum.complete_transaction`; the `sockets` service consumes them and fans out Socket.IO events to per-user rooms.
- **Reliable async ORM** — SQLAlchemy 2.0 async session per request, `asyncpg` driver, Alembic migrations, and a `TransactionManager`/`Flusher` port abstraction that decouples use-cases from the DB session.
- **Blockchain confirmation tracking** — every broadcast transaction hash is stored in a Redis **sorted set** (score = timestamp). A WebSocket listener (Infura `eth_subscribe newHeads`) detects mined blocks and marks transactions complete; a reconciliation task rescans hashes idle for >120s every 60s, so transactions that missed the block stream are still finalized.
- **Secure key handling** — private keys are encrypted at rest (AES-256-CFB) and only decrypted at the moment a transaction is signed inside the `ethereum` service.
- **Scale-ready real time** — Socket.IO runs with a Redis `AsyncRedisManager`, enabling horizontal scaling of the sockets service.

## Quick Start / Getting Started

### Prerequisites

- Python 3.13+ and [Poetry](https://python-poetry.org/)
- Node.js 20+ and npm (for the frontend)
- Docker & Docker Compose (optional, for containerized run)
- PostgreSQL, MongoDB, Redis, RabbitMQ instances (or run them via Docker)

### Local setup

Each backend service is a separate Python package managed with Poetry.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vlad1m1r0v/CryptoWallet.git
   cd CryptoWallet
   ```

2. **Configure environment variables** for each service by copying the examples:

   ```bash
   cp backend/rest_api/.env.example backend/rest_api/.env
   cp backend/ethereum/.env.example backend/ethereum/.env
   cp backend/ibay/.env.example backend/ibay/.env
   cp backend/sockets/.env.example backend/sockets/.env
   cp frontend/.env.example frontend/.env
   ```

   Then fill in your credentials (PostgreSQL, RabbitMQ, Redis, MongoDB, Infura, Etherscan, Mailjet, S3).

3. **Generate JWT signing keys** (required by `rest_api` and `sockets`):

   ```bash
   cd backend/rest_api && make certificates
   cd backend/sockets && make certificates
   ```

4. **Install dependencies and run the REST API:**

   ```bash
   cd backend/rest_api
   poetry install
   poetry run make upgrade   # run Alembic migrations
   poetry run make cli       # seed the default Sepolia ETH asset
   poetry run make server    # uvicorn on :8000
   ```

5. **Run the remaining services** (each in its own terminal):

   ```bash
   # Ethereum integration (FastStream consumer + block listener)
   cd backend/ethereum && poetry install && poetry run make faststream

   # Marketplace fulfillment
   cd backend/ibay && poetry install && poetry run make upgrade && poetry run make faststream

   # Sockets: Socket.IO gateway + FastStream consumer
   cd backend/sockets && poetry install && poetry run make socketio && poetry run make faststream

   # REST API background worker + scheduler
   cd backend/rest_api && poetry run make worker && poetry run make scheduler
   ```

6. **Run the frontend:**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker

Every service ships a production `Dockerfile` (see `backend/*/deploy/*/Dockerfile`, `backend/ibay/deploy/Dockerfile`, `backend/ethereum/deploy/Dockerfile`, `frontend/Dockerfile`). To run the whole stack with Docker Compose:

```bash
docker-compose up --build
```

> **Note:** the repository provides per-service Dockerfiles and `.env.example` files, but no `docker-compose.yml` is committed yet. Define one that wires up PostgreSQL, MongoDB, Redis, RabbitMQ, and the five application services using the provided `Dockerfile`s and environment examples.

## API Endpoints Overview

Interactive API documentation (Swagger UI) is auto-generated by FastAPI at [`/docs`](http://localhost:8000/docs) (ReDoc at `/redoc`).

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Authenticate and receive a JWT access token |
| `GET` | `/profiles/me` | Get the authenticated user's profile |
| `POST` | `/wallets` | Request creation of a new Ethereum wallet |
| `GET` | `/wallets` | List the user's wallets |
| `POST` | `/wallets/import` | Import an existing wallet from a private key |
| `POST` | `/transactions` | Send ETH to an address |
| `GET` | `/transactions` | List wallet transactions (paginated, sortable) |
| `POST` | `/products` | Publish a marketplace product |
| `POST` | `/orders` | Place an order and pay for it on-chain |

## Future Roadmap

1. **Delivery guarantees** — introduce an outbox pattern and idempotent consumers so events are never lost when RabbitMQ or a database transaction fails.
2. **Automated testing & CI** — add unit/integration/E2E test suites for all four services and a GitHub Actions pipeline (lint, type-check, test, build images).
3. **Observability & scaling** — add OpenTelemetry tracing, Prometheus metrics, structured logging, and swap the simulated marketplace fulfillment for a real external payment/fraud flow, plus true horizontal scaling for the sockets tier.

---

*License: this repository is currently unlicensed — see the project author for usage terms.*
