# coding: utf-8

from generator.metaprog.types import Void
from generator.metaprog.types import Schema


class DatabaseEntrySchema():
    def __init__(self,
        phone_number: str,
        country_code: str,
        operator_code: str,
        generated_suffix: str
    ):
        self.__phone_number: str = phone_number
        self.__country_code: str = country_code
        self.__operator_code: str = operator_code
        self.__generated_suffix: str = generated_suffix
        self.__build_schema()


    def __build_schema(self) -> Void:
        phone_number: str = self.__phone_number
        country_code: str = self.__country_code
        operator_code: str = self.__operator_code
        generated_suffix: str = self.__generated_suffix

        schema: Schema = Schema({
            "phone_number": phone_number,
            "country_code": country_code,
            "operator_code": operator_code,
            "generated_suffix": generated_suffix
        })
        self._schema: Schema = schema
