from pydantic import BaseModel


class Sentence(BaseModel):
    body: str
    path: str


class SearchResult(BaseModel):
    sentence: Sentence
    score: float
