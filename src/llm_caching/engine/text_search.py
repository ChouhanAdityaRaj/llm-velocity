from rapidfuzz import process, fuzz
from src.llm_caching.constants import constants


class TextSearch:
    @staticmethod
    def search_text(data_list: list[str], key: str) -> int | None:
        if not data_list:
            return None

        result = process.extractOne(
            query=key,
            choices=data_list,
            scorer=fuzz.ratio
        )

        if result is None:
            return None

        _, score, index = result

        if score < constants.TEXT_MATCH_MIN_SCORE:
            return None

        return index