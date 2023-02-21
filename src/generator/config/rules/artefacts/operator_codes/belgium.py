# coding: utf-8


from generator.internal_lib.list import uniq


OPERATORS_CODES = {
    "MOBILE": uniq([
        "999"
    ]),

    "DESK": uniq(
        ["1", "2", "3", "4", "5"]
    )
}
