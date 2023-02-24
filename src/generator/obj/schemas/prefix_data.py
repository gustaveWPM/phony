# coding: utf-8


from generator.metaprog.types import Void, Schema

from typing import List


class PrefixDataSchema():
    def __init__(self,
        country_code: str,
        operator_desk_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        self.__country_code = country_code
        self.__build_schema(operator_desk_codes, operator_mobile_codes)


    def __build_schema(self, operator_desk_codes, operator_mobile_codes) -> Void:
        schema = Schema({
            "country_code": self.__country_code,
            "operator_codes": {
                "desk": operator_desk_codes,
                "mobile": operator_mobile_codes
            }
        })
        self._schema = schema
