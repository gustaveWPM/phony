# coding: utf-8


from generator.obj.schemas.prefix_data import PrefixDataSchema

from typing import List, Optional


class PrefixData(PrefixDataSchema):
    def __init__(self,
        country_code: str,
        operator_landline_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        super().__init__(country_code, operator_landline_codes, operator_mobile_codes)


    def country_code(self, value: Optional[str] = None) -> Optional[str]:
        if value is None:
            return self._schema["country_code"]
        self._schema["country_code"] = value


    def operator_mobile_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self._schema["operators_codes"]["mobile"]
        self._schema["operators_codes"]["mobile"] = value


    def operator_landline_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self._schema["operators_codes"]["landline"]
        self._schema["operators_codes"]["landline"] = value


    def force_operators_codes(self, data: List[str]):
        self.operator_landline_codes(data)
        self.operator_mobile_codes(data)
