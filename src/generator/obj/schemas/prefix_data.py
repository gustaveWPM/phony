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
        self._operator_desk_codes = operator_desk_codes
        self._operator_mobile_codes = operator_mobile_codes
        self.__build_schema()


    def __build_schema(self) -> Void:
        schema = Schema({
            "country_code": self.__country_code,
            "operator_codes": {
                "desk": self._operator_desk_codes,
                "mobile": self._operator_mobile_codes
            }
        })
        self._schema = schema
