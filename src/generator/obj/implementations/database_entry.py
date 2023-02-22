# coding: utf-8


from generator.obj.schemas.database_entry import DatabaseEntrySchema
from generator.metaprog.types import WeakSchema


class DatabaseEntry(DatabaseEntrySchema):
    def __init__(self,
        phone_number: str,
        country_code: str,
        operator_code: str,
        generated_suffix: str
    ):
        super().__init__(phone_number, country_code, operator_code, generated_suffix)


    # * ... Because of Pymongo's dynamic '_id' generation...
    def schema(self) -> WeakSchema:
        return self._schema
