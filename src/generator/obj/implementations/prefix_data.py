# coding: utf-8


from generator.obj.schemas.prefix_data import PrefixDataSchema

from typing import List, Optional


class PrefixData(PrefixDataSchema):
    def __init__(self,
        country_code: str,
        operator_desk_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        super().__init__(country_code, operator_desk_codes, operator_mobile_codes)


    def country_code(self, value: Optional[str] = None) -> Optional[str]:
        if value is None:
            return self._schema["country_code"]
        self._schema["country_code"] = value


    def operator_mobile_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self._schema["operator_codes"]["mobile"]
        self._schema["operator_codes"]["mobile"] = value


    def operator_desk_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self._schema["operator_codes"]["desk"]
        self._schema["operator_codes"]["desk"] = value


    def force_operator_codes(self, data: List[str]):
        self._operator_desk_codes = []
        self._operator_mobile_codes = data
