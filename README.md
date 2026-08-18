# ResearchGraph — Academic Collaboration Network

A graph-powered web application for exploring academic research connections, built with **CognoDB** (openCypher/Bolt), **FastAPI**, and **React**.

![Dashboard](screenshots/dashboard.png)

## Why a Graph Database?

Academic research is inherently a network problem. Papers cite other papers, authors collaborate across institutions, and research topics form interdisciplinary bridges. These connections are the *data* — not metadata or foreign keys.

A relational schema would require multiple join tables and recursive CTEs to answer questions like:
- "Find the shortest collaboration path between two researchers"
- "Which papers influenced this paper through citation chains?"
- "Who are potential collaborators based on shared research interests?"

These are **multi-hop traversals** — the graph database's core strength. In CognoDB, a query like "find collaboration path" is a single `shortestPath()` call, while the same query in PostgreSQL would require recursive CTEs with exponential complexity.

### Specific examples where graph wins:

| Query | Graph (Cypher) | Relational (SQL) |
|-------|---------------|-------------------|
| Collaboration path | `shortestPath((a1)-[*]-(a2))` | Recursive CTE with depth limit |
| Citation chain | `(paper)-[:CITES*1..3]->(end)` | 3+ self-joins or recursive CTE |
| Influence network | Multi-hop pattern match | Multiple nested subqueries |
| Recommended collaborators | Topic-based path matching | Complex JOINs + aggregation |

## Data Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA MODEL                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    TAGGED_WITH    ┌──────────┐                   │
│  │  Paper   │──────────────────▶│   Topic   │                   │
│  └──────────┘                   └──────────┘                   │
│       │                                                     │
│       │ CITES                                              │
│       │ (self-                                             │
│       │  referential)                                      │
│       ▼                                                     │
│  ┌──────────┐    AUTHORED_BY    ┌──────────┐                │
│  │  Paper   │──────────────────▶│  Author   │                │
│  └──────────┘                   └──────────┘                │
│                                     │                        │
│                             AFFILIATED_WITH                   │
│                                     │                        │
│                                     ▼                        │
│                                ┌──────────────┐              │
│                                │ Institution  │              │
│                                └──────────────┘              │
│                                                                 │
│  ┌──────────┐  COLLABORATES_WITH  ┌──────────┐               │
│  │  Author  │◀───────────────────▶│  Author   │               │
│  └──────────┘                      └──────────┘               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  NODE TYPES: Paper, Author, Institution, Topic                 │
│  RELATIONSHIP TYPES: CITES, AUTHORED_BY, TAGGED_WITH,         │
│                      AFFILIATED_WITH, COLLABORATES_WITH        │
└─────────────────────────────────────────────────────────────────┘
```

### Node Properties

| Node | Properties |
|------|-----------|
| Paper | `id`, `title`, `year`, `abstract`, `citations_count` |
| Author | `id`, `name`, `h_index` |
| Institution | `id`, `name`, `country`, `ranking` |
| Topic | `id`, `name`, `category` |

## Key Queries

### 1. Multi-Hop: Collaboration Path (2+ hops)
```cypher
MATCH path = shortestPath(
    (a1:Author {id: $from_id})-[:AUTHORED_BY|COLLABORATES_WITH*1..6]-(a2:Author {id: $to_id}
))
RETURN path
```
Finds the shortest path connecting two researchers through co-authorship relationships.

### 2. Awkward in Relational: Influence Network (3-hop citation chain)
```cypher
MATCH (target:Paper {id: $paper_id})
MATCH (influencer:Paper)-[:CITES*1..3]->(target)
RETURN influencer
```
Finds all papers that influenced a given paper through up to 3 levels of citations. Requires recursive traversal that relational databases handle poorly.

### 3. Recommended Collaborators (topic-based path matching)
```cypher
MATCH (a:Author {id: $author_id})<-[:AUTHORED_BY]-(p:Paper)-[:TAGGED_WITH]->(t:Topic)
MATCH (other:Author)<-[:AUTHORED_BY]-(p2:Paper)-[:TAGGED_WITH]->(t)
WHERE other <> a AND NOT (a)-[:COLLABORATES_WITH]-(other)
RETURN other, COLLECT(DISTINCT t.name) AS shared_topics
```

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A CognoDB Cloud instance (free tier)

### 1. Create CognoDB Instance

1. Sign up at [console.cognodb.com/signup](https://console.cognodb.com/signup)
2. Create a free (c0) instance
3. Save your connection URI (`bolt+s://...`) and password

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your CognoDB credentials
```

```
COGNODB_URI=bolt+s://your-instance.databases.cognodb.cloud
COGNODB_USER=cognodb
COGNODB_PASSWORD=your_password_here
```

### 3. Seed the Database

```bash
cd scripts
pip install -r requirements.txt
python seed.py
```

### 4. Run the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 5. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│         (Vite + Tailwind CSS + React Router)             │
│  Pages: Dashboard, Papers, Authors, Institutions,       │
│         Topics, Explorer (collaboration paths,           │
│         influence networks, recommendations)             │
└─────────────────────┬───────────────────────────────────┘
                      │ REST API (JSON)
┌─────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend                          │
│           (Python 3.10+ / Uvicorn)                       │
│  Routes: /api/papers, /api/authors, /api/institutions,  │
│          /api/topics, /api/explore, /api/search          │
│  All queries parameterized via Neo4j driver              │
└─────────────────────┬───────────────────────────────────┘
                      │ Bolt 5.x protocol
┌─────────────────────▼───────────────────────────────────┐
│              CognoDB (Neo4j-compatible)                  │
│  openCypher queries · Full-text indexes                  │
│  Free tier: 0.5 vCPU, 256MB RAM, 1GB disk               │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
wexaai/
├── backend/
│   ├── main.py          # FastAPI application & routes
│   ├── database.py      # Neo4j driver connection
│   ├── queries.py       # All Cypher queries
│   ├── models.py        # Pydantic models
│   ├── config.py        # Settings (env vars)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Router setup
│   │   ├── main.jsx             # Entry point
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Route pages
│   │   └── lib/                 # API client & hooks
│   ├── index.html
│   ├── package.json
│   └── tailwind.config.js
├── scripts/
│   ├── seed.py          # Database seeding script
│   └── requirements.txt
├── .env.example         # Environment template
├── .gitignore
└── README.md
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `COGNODB_URI` | Bolt connection URI | `bolt+s://xxx.databases.cognodb.cloud` |
| `COGNODB_USER` | Database username | `cognodb` |
| `COGNODB_PASSWORD` | Database password | (from console) |

**Never commit `.env` to version control.**

## Screenshots

![Dashboard](screenshots/dashboard.png)
![Papers](screenshots/papers.png)
![Author Detail](screenshots/author-detail.png)
![Collaboration Path](screenshots/collaboration-path.png)
![Influence Network](screenshots/influence-network.png)

## Tech Stack

- **Database**: CognoDB (openCypher, Bolt 5.x)
- **Backend**: Python, FastAPI, neo4j driver
- **Frontend**: React 18, Vite, Tailwind CSS, React Router
- **Hosting**: (Vercel / Render / Railway)
