# coding: utf-8


from generator.metaprog.types import Void, WeakSchema


class DatabaseEntrySchema():
    def __init__(self,
        phone_number: str,
        country_code: str,
        operator_code: str,
        generated_suffix: str
    ):
        self._schema: WeakSchema = self.__build_schema(phone_number, country_code, operator_code, generated_suffix)


    # * ... Because of Pymongo's dynamic '_id' generation...
    def __build_schema(self,
        phone_number: str,
        country_code: str,
        operator_code: str,
        generated_suffix: str
    ) -> WeakSchema:
        return WeakSchema({
            "phone_number": int(phone_number),
            "country_code": country_code,
            "operator_code": operator_code,
            "generated_suffix": generated_suffix
        })
