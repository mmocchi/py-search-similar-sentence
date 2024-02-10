import sqlparse

from py_search_similar_sentence.searcher.models import Sentence, SearchResult
from py_search_similar_sentence.searcher.similar_sentence_searcher import (
    SimilarSentenceSearcher,
)


ignore_token_types = [
    "Token.Comment.Single",
    "Token.Comment.Multiline",
    "Token.Text.Whitespace",
    "Token.Punctuation",
]


def _get_sql_tokens(query: str) -> list[str]:
    parsed_queries = sqlparse.parse(query)
    tokens = [
        t.value
        for t in list(parsed_queries[0].flatten())
        if str(t.ttype) not in ignore_token_types
    ]
    return tokens


def get_normalized_sql(query: str) -> str:
    return format_sql(" ".join(_get_sql_tokens(query)))

def format_sql(sql: str) -> str:
    return sqlparse.format(sql, reindent=True, keyword_case="upper")

class SimilarSQLSearcher:
    def __init__(self, candidate_sqls: list[Sentence]):
        self.candidate_sqls = candidate_sqls
        self.parsed_candidate_sqls = [
            Sentence(body=get_normalized_sql(sql.body), path=sql.path)
            for sql in candidate_sqls
        ]

        self._seacher = SimilarSentenceSearcher(self.parsed_candidate_sqls)

    def get_similar_sql(self, sql_sentence: Sentence, n: int = 3, threshold: float = 0.5) -> list[SearchResult]:
        target_sql = Sentence(
            body=get_normalized_sql(sql_sentence.body), path=sql_sentence.path
        )
        similar_sentences = self._seacher.get_similar_sentences(target_sql, n=n, threshold=threshold)
        resutls = [
            SearchResult(
                sentence=Sentence(body=s.sentence.body, path=s.sentence.path), score=s.score
            )
            for s in similar_sentences
        ]
        return resutls
