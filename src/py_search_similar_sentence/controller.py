import glob
import pathlib

import pandas as pd
from tabulate import tabulate

from py_search_similar_sentence.searcher.models import Sentence, SearchResult
from py_search_similar_sentence.searcher.similar_sql_searcher import SimilarSQLSearcher


def get_default_files() -> list[str]:
    project_path = pathlib.Path(__file__).parent.parent.parent.absolute()
    return get_files(project_path.joinpath(pathlib.Path("sample/train/")))

def get_files(directory_path: pathlib.Path) -> list[str]:
    return  glob.glob(str(directory_path.joinpath(pathlib.Path('**/*.sql')).absolute()), recursive=True)


def get_file_text(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def get_similar_sqls(sql: str, n: int = 3, threshold: float = 0.5) -> list[SearchResult]:
    target_text = Sentence(body=sql, path="__target__")

    candidate_sqls = get_candidate_sqls()

    searcher = SimilarSQLSearcher(candidate_sqls)
    return searcher.get_similar_sql(target_text, n=n, threshold=threshold)


def get_candidate_sqls() -> list[Sentence]:
    sentences = []
    for path in get_default_files():
        contents = get_file_text(path)
        sentences.append(Sentence(body=contents, path=path))
    return sentences


def print_similar_sqls(sql: str, n: int = 3, threshold: float = 0.5) -> None:
    """
    Print similar SQLs
    """
    search_results = get_similar_sqls(sql, n=n, threshold=threshold)

    print(f'Input SQL(formatted): {sql}')
    if len(search_results) == 0:
        print("No similar SQLs found.")
        return
    
    result_df = pd.DataFrame([{'SQL(formatted)': r.sentence.body, 'score': r.score} for r in search_results])
    result_df['score'] = result_df['score'].round(2)
    print(tabulate(result_df, headers='keys', tablefmt='grid'))


def sample():
    sql = "SELECT col1 FROM hoge WHERE id = 00 AND age = 100 AND name = 'fuga';"
    print_similar_sqls(sql, 4, 0.3)
