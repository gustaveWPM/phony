# coding: utf-8


from generator.metaprog.types import Void, WeakSchema


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
        self._schema: WeakSchema = self.__build_schema()


    # * ... Because of Pymongo's dynamic '_id' generation...
    def __build_schema(self) -> WeakSchema:
        return WeakSchema({
            "phone_number": self.__phone_number,
            "country_code": self.__country_code,
            "operator_code": self.__operator_code,
            "generated_suffix": self.__generated_suffix
        })
