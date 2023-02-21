# coding: utf-8


from generator.obj.schemas.metadatas import MetadatasSchema
from generator.metaprog.types import Schema


class Metadatas(MetadatasSchema):
    def __init__(self,
        phone_number_suffix: str,
        phone_number_country_code: str,
        phone_number_operator_code: str
    ):
        super().__init__(
            phone_number_suffix,
            phone_number_country_code,
            phone_number_operator_code
        )


    def schema(self) -> Schema:
        return self._schema
