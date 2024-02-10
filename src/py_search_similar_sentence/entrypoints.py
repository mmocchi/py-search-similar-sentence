import click

from py_search_similar_sentence.controller import print_similar_sqls as print_similar_sqls_, sample

@click.group()
def cli():
    pass

@cli.command()
def hello():
    sample()

@cli.command()
@click.argument('sql')
@click.option("--n", "-n", default=3, help="Number of similar SQLs to search", type=click.IntRange(1, 128))
@click.option("--threshold", "-t", default=0.5, help="Threshold of similarity", type=click.FloatRange(0, 1))
def print_similar_sqls(sql: str, n: int, threshold: float):
    print_similar_sqls_(sql, n=n, threshold=threshold)

