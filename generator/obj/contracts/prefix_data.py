# coding: utf-8

from typing import List


class PrefixData:
    def __init__(self,
        country_code: str,
        operator_desk_codes: List[str],
        operator_mobile_codes: List[str]
    ):
        self.__country_code = country_code
        self.__operator_desk_codes = operator_desk_codes
        self.__operator_mobile_codes = operator_mobile_codes
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
        self.__dict = self._dictionnary_builder()


    def get_country_code(self) -> str:
        return self.__dict["COUNTRY_CODE"]


    def get_operator_mobile_codes(self) -> List[str]:
        return self.__dict["OPERATOR_CODES"]["MOBILE"]


    def get_operator_desk_codes(self) -> List[str]:
        return self.__dict["OPERATOR_CODES"]["DESK"]


    def get_operator_codes_union(self) -> List[str]:
        operator_desk_codes = self.get_operator_desk_codes()
        operator_mobile_codes = self.get_operator_mobile_codes()
        union = operator_desk_codes + operator_mobile_codes
        return union
