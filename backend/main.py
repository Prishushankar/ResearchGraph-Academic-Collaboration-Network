from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import get_driver, close_driver, run_query
import queries
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_driver()
        create_indexes()
    except Exception as e:
        logger.warning(f"Could not connect to database on startup: {e}")
    yield
    close_driver()


app = FastAPI(
    title="ResearchGraph API",
    description="Academic Research Collaboration Network",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_indexes():
    try:
        run_query("CREATE FULLTEXT INDEX search_index IF NOT EXISTS FOR (n:Paper|Author|Institution|Topic) ON EACH [n.title, n.name]")
        run_query("CREATE INDEX paper_id IF NOT EXISTS FOR (p:Paper) ON (p.id)")
        run_query("CREATE INDEX author_id IF NOT EXISTS FOR (a:Author) ON (a.id)")
        run_query("CREATE INDEX institution_id IF NOT EXISTS FOR (i:Institution) ON (i.id)")
        run_query("CREATE INDEX topic_id IF NOT EXISTS FOR (t:Topic) ON (t.id)")
    except Exception as e:
        logger.warning(f"Index creation: {e}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if "connection" in str(exc).lower() or "driver" in str(exc).lower():
        return JSONResponse(
            status_code=503,
            content={"detail": "Database is unreachable. Please try again later."},
        )
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/api/stats")
def get_stats():
    try:
        result = run_query(queries.GET_GRAPH_STATS)
        return result[0] if result else {}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/papers")
def get_papers(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return run_query(queries.GET_ALL_PAPERS, {"limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/papers/{paper_id}")
def get_paper(paper_id: str):
    try:
        result = run_query(queries.GET_PAPER_BY_ID, {"id": paper_id})
        if not result:
            raise HTTPException(status_code=404, detail="Paper not found")
        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/authors")
def get_authors(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return run_query(queries.GET_ALL_AUTHORS, {"limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/authors/{author_id}")
def get_author(author_id: str):
    try:
        result = run_query(queries.GET_AUTHOR_BY_ID, {"id": author_id})
        if not result:
            raise HTTPException(status_code=404, detail="Author not found")
        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/institutions")
def get_institutions(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return run_query(queries.GET_ALL_INSTITUTIONS, {"limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/institutions/{institution_id}")
def get_institution(institution_id: str):
    try:
        result = run_query(queries.GET_INSTITUTION_BY_ID, {"id": institution_id})
        if not result:
            raise HTTPException(status_code=404, detail="Institution not found")
        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/topics")
def get_topics(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return run_query(queries.GET_ALL_TOPICS, {"limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/collaboration-path")
def find_collaboration_path(from_id: str = Query(...), to_id: str = Query(...)):
    try:
        result = run_query(queries.FIND_COLLABORATION_PATH, {"from_id": from_id, "to_id": to_id})
        if not result:
            return {"path_nodes": [], "path_relationships": [], "path_length": 0}
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/citation-chain/{paper_id}")
def find_citation_chain(paper_id: str, depth: int = Query(default=3, ge=1, le=5)):
    try:
        result = run_query(queries.FIND_CITATION_CHAIN, {"paper_id": paper_id, "depth": depth})
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/influence-network/{paper_id}")
def find_influence_network(paper_id: str, limit: int = Query(default=20, ge=1, le=50)):
    try:
        return run_query(queries.FIND_INFLUENCE_NETWORK, {"paper_id": paper_id, "limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/recommendations/{author_id}")
def recommend_collaborators(author_id: str, limit: int = Query(default=10, ge=1, le=30)):
    try:
        return run_query(queries.RECOMMEND_COLLABORATORS, {"author_id": author_id, "limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/interdisciplinary")
def find_interdisciplinary(min_topics: int = Query(default=3, ge=2), limit: int = Query(default=20)):
    try:
        return run_query(queries.FIND_INTERDISCIPLINARY_AUTHORS, {"min_topics": min_topics, "limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = Query(default=20)):
    try:
        return run_query(queries.SEARCH, {"query": q, "limit": limit})
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")


@app.get("/api/health")
def health_check():
    try:
        run_query("RETURN 1 AS ok")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)},
        )
