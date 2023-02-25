# coding: utf-8


from generator.metaprog.types import Schema

from typing import List


class PrefixDataSchema():
    def __init__(self,
        country_code: str,
        operator_landline_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        self._schema = self.__build_schema(country_code, operator_landline_codes, operator_mobile_codes)


    def __build_schema(self,
        country_code,
        operator_landline_codes,
        operator_mobile_codes
    ) -> Schema:
        return Schema({
            "country_code": country_code,
            "operator_codes": {
                "landline": operator_landline_codes,
                "mobile": operator_mobile_codes
            }
        })
