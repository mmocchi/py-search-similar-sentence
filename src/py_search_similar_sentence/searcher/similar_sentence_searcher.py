import difflib
import Levenshtein
from tqdm import tqdm

from py_search_similar_sentence.searcher.models import Sentence, SearchResult


def calc_gestalt_score(word1: str, word2: str) -> float:
    return difflib.SequenceMatcher(None, word1, word2).ratio()


def calc_levenshtein_score(word1: str, word2: str) -> float:
    return 1 - Levenshtein.ratio(word1, word2)


def calc_jaro_winkler_score(word1: str, word2: str) -> float:
    return Levenshtein.jaro_winkler(word1, word2)


class SimilarSentenceSearcher:
    """
    Search similar sentences from candidate sentences"""

    def __init__(self, candidate_sentences: list[Sentence]):
        self.__candidate_sentences = candidate_sentences

    def __calc_similar_score(self, sentence1: Sentence, sentence2: Sentence) -> float:
        gestalt = calc_gestalt_score(sentence1.body, sentence2.body)
        jaro_winkler = calc_jaro_winkler_score(sentence1.body, sentence2.body)
        return (gestalt + jaro_winkler) / 2

    def get_similar_sentences(
        self, target_sentence: Sentence, n: int = 3, threshold: float = 0.5
    ) -> list[SearchResult]:
        """
        Get similar sentences from candidate sentences

        Args:
            target_sentence (Sentence): target sentence
            n (int, optional): number of similar sentences to search. Defaults to 3.
            threshold (float, optional): threshold of similarity. Defaults to 0.5.
        """
        results = []
        for i, sentence in tqdm(enumerate(self.__candidate_sentences)):
            score = self.__calc_similar_score(target_sentence, sentence)
            if score < threshold:
                continue

            results.append(SearchResult(sentence=sentence, score=score))

        # sort by similarity score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:n]
