# coding: utf-8

from typing import Optional, List
from generator.obj.contracts.prefix_data import PrefixData
from generator.metaprog.types import Void


def slice_op_codes(metadatas: Optional[dict], prefix_data: PrefixData) -> Void:
    if metadatas is None:
        return

    needle: str = metadatas["phone_number_operator_code"]

    operator_desk_codes: List[str] = prefix_data.operator_desk_codes()
    operator_mobile_codes: List[str] = prefix_data.operator_mobile_codes()

    if needle in operator_desk_codes:
        index: int = operator_desk_codes.index(needle)
        prefix_data.operator_desk_codes(operator_desk_codes[index:])
        prefix_data.start_with_desk(True)

    if needle in operator_mobile_codes:
        index: int = operator_mobile_codes.index(needle)
        prefix_data.operator_mobile_codes(operator_mobile_codes[index:])
        prefix_data.start_with_desk(False)
