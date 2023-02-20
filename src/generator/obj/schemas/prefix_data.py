# coding: utf-8

from generator.metaprog.types import Void, Schema
from typing import List


class PrefixDataSchema():
    def __init__(self,
        country_code: str,
        operator_desk_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        self.__country_code: str = country_code
        self._operator_desk_codes: List[str] = operator_desk_codes
        self._operator_mobile_codes: List[str] = operator_mobile_codes
        self.__build_schema()


    def __build_schema(self) -> Void:
        country_code: str = self.__country_code
        operator_desk_codes: List[str] = self._operator_desk_codes
        operator_mobile_codes: List[str] = self._operator_mobile_codes

        schema: Schema = Schema({
            "country_code": country_code,
            "operator_codes": {
                "desk": operator_desk_codes,
                "mobile": operator_mobile_codes
            }
        })
        self._schema: Schema = schema
