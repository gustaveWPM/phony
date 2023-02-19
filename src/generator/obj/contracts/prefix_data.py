# coding: utf-8

from typing import List, Optional


class PrefixData:
    def __init__(self,
        country_code: str,
        operator_desk_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        self.__country_code: str = country_code
        self.__operator_desk_codes: List[str] = operator_desk_codes
        self.__operator_mobile_codes: List[str] = operator_mobile_codes
        self.__start_with_desk: bool = False
        self._dictionnary_builder()


    def _dictionnary_builder(self) -> None:
        country_code = self.__country_code
        operator_desk_codes = self.__operator_desk_codes
        operator_mobile_codes = self.__operator_mobile_codes

        dict_schema = {
            "COUNTRY_CODE": country_code,
            "OPERATOR_CODES": {
                "DESK": operator_desk_codes,
                "MOBILE": operator_mobile_codes
            }
        }
        self.__dict: dict = dict_schema


    def country_code(self, value: Optional[str] = None) -> Optional[str]:
        if value is None:
            return self.__dict["COUNTRY_CODE"]
        self.__dict["COUNTRY_CODE"] = value


    def operator_mobile_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self.__dict["OPERATOR_CODES"]["MOBILE"]
        self.__dict["OPERATOR_CODES"]["MOBILE"] = value


    def operator_desk_codes(self, value: Optional[List[str]] = None) -> Optional[List[str]]:
        if value is None:
            return self.__dict["OPERATOR_CODES"]["DESK"]
        self.__dict["OPERATOR_CODES"]["DESK"] = value


    def start_with_desk(self, value: Optional[bool] = None) -> Optional[bool]:
        if value is None:
            return self.__start_with_desk
        self.__start_with_desk = value


    def force_operator_codes(self, data: List[str]):
        self.__operator_desk_codes = []
        self.__operator_mobile_codes = data
