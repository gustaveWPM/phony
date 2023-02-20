# coding: utf-8

from generator.metaprog.types import Void, Schema


class MetadatasSchema():
    def __init__(self,
        phone_number_suffix: str,
        phone_number_country_code: str,
        phone_number_operator_code: str
    ):
        self.__phone_number_suffix: str = phone_number_suffix
        self.__phone_number_country_code: str = phone_number_country_code
        self.__phone_number_operator_code: str = phone_number_operator_code
        self.__build_schema()


    def __build_schema(self) -> Void:
        phone_number_suffix: str = self.__phone_number_suffix
        phone_number_country_code: str = self.__phone_number_country_code
        phone_number_operator_code: str = self.__phone_number_operator_code

        schema: Schema = Schema({
            "phone_number_suffix": phone_number_suffix,
            "phone_number_country_code": phone_number_country_code,
            "phone_number_operator_code": phone_number_operator_code
        })
        self._schema: Schema = schema
