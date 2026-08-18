from pydantic import BaseModel
from typing import Optional


class Paper(BaseModel):
    id: str
    title: str
    year: int
    abstract: Optional[str] = None
    citations_count: int = 0


class Author(BaseModel):
    id: str
    name: str
    h_index: int = 0
    institution: Optional[str] = None


class Institution(BaseModel):
    id: str
    name: str
    country: str = ""
    ranking: int = 0


class Topic(BaseModel):
    id: str
    name: str
    category: str = ""


class CollaborationPath(BaseModel):
    path: list
    length: int


class CitationChain(BaseModel):
    chain: list
    depth: int


class GraphStats(BaseModel):
    papers: int
    authors: int
    institutions: int
    topics: int
    citations: int
    authorships: int
