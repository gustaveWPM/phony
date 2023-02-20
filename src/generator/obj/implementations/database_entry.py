# coding: utf-8

from generator.obj.schemas.database_entry import DatabaseEntrySchema
from generator.metaprog.types import Schema


class DatabaseEntry(DatabaseEntrySchema):
    def __init__(self,
        phone_number: str,
        country_code: str,
        operator_code: str,
        generated_suffix: str
    ):
        super().__init__(phone_number, country_code, operator_code, generated_suffix)


    def schema(self) -> Schema:
        return self._schema
