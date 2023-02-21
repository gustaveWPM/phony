# coding: utf-8

from generator.obj.implementations.singletons.generator_base import GeneratorBase
from generator.obj.implementations.prefix_data import PrefixData
from generator.metaprog.types import Void
from generator.sys.error import terminate
from generator.debug.logger import debug_logger as debug_logger
from generator.debug.vocab import VOCAB as DEBUG_VOCAB
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
import generator.phone_range_limit as limit
from generator.obj.implementations.database_entry import DatabaseEntry

from typing import Optional, List
# from numba import jit # * ... {ToDo} Optimize MongoDB updates, then benchmark JIT

class Generator(GeneratorBase):
    @staticmethod
    def __append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
        number_as_string: str = str(number)
        if number >= magnitude:
            return number_as_string
        number_len: int = len(number_as_string)
        number_of_zeros_to_append: int = abs(ndigits - number_len)
        phone_suffix: str = '0' * number_of_zeros_to_append + number_as_string
        return phone_suffix


    def __start_with_desk(self, value: Optional[bool] = None) -> Optional[bool]:
        if value is None:
            return self._start_with_desk
        self._start_with_desk = value

    # @jit(target_backend='cuda', forceobj=True) # * ... {ToDo} Optimize MongoDB updates, then benchmark JIT
    def __do_generate_range(self, r: range, block_len: int, magnitude: int, cur_op_code: str, country_code: str):
        prefix: str = country_code + cur_op_code

        for current_iteration in r:
            cur_phone_number_suffix: str = self.__append_heading_zeros(
                current_iteration, block_len, magnitude)
            if not self._reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix):
                cur_phone_number: str = prefix + cur_phone_number_suffix
                database_entry: DatabaseEntry = DatabaseEntry(
                    cur_phone_number, country_code, cur_op_code, cur_phone_number_suffix
                )

                self._database.save_phone_number(database_entry)
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_GENERATED_PHONE_NUMBERS:
                    debug_logger("GENERATED_PHONE_NUMBER", f"{cur_phone_number} ; op_code: {cur_op_code}")
            elif DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_PHONE_NUMBERS:
                cur_phone_number: str = prefix + cur_phone_number_suffix
                debug_logger("REJECTED_PHONE_NUMBER", cur_phone_number)


    def __do_generate_loop(self, country_code: str, op_codes: List[str], metadatas: Optional[dict]):
        for cur_op_code in op_codes:
            if self._is_banned_op_code(cur_op_code):
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_OPERATOR_CODES:
                    debug_logger("REJECTED_OPERATOR_CODE", cur_op_code)
                continue
            block_len: int = limit.compute_range_len(cur_op_code)
            magnitude: int = 10 ** (block_len - 1)
            last_iteration: int = limit.compute_range_end(cur_op_code)
            first_iteration: int = limit.compute_range_start(metadatas, cur_op_code, magnitude)
            r = range(first_iteration, last_iteration)
            self.__do_generate_range(r, block_len, magnitude, cur_op_code, country_code)


    def __do_generate(self, prefix_data: PrefixData, metadatas: dict) -> Void:
        country_code: str = prefix_data.country_code()
        op_codes_a: List[str] = []
        op_codes_b: List[str] = []

        if self.__start_with_desk():
            op_codes_a = prefix_data.operator_desk_codes()
            op_codes_b = prefix_data.operator_mobile_codes()
        else:
            op_codes_a = prefix_data.operator_mobile_codes()
            op_codes_b = prefix_data.operator_desk_codes()

        self.__do_generate_loop(country_code, op_codes_a, metadatas)
        self.__do_generate_loop(country_code, op_codes_b, metadatas)


    def __slice_op_codes(
        self,
        metadatas: Optional[dict],
        prefix_data: PrefixData,
    ) -> Void:
        if metadatas is None:
            return

        needle: str = metadatas["phone_number_operator_code"]

        operator_desk_codes: List[str] = prefix_data.operator_desk_codes()
        operator_mobile_codes: List[str] = prefix_data.operator_mobile_codes()

        if needle in operator_desk_codes:
            index: int = operator_desk_codes.index(needle)
            prefix_data.operator_desk_codes(operator_desk_codes[index:])
            self.__start_with_desk(True)

        if needle in operator_mobile_codes:
            index: int = operator_mobile_codes.index(needle)
            prefix_data.operator_mobile_codes(operator_mobile_codes[index:])
            self.__start_with_desk(False)


    def __smart_reload(self, metadatas: Optional[dict], prefix_data: PrefixData) -> Void:
        self.__slice_op_codes(metadatas, prefix_data)


    def process(self) -> Void:
        prefix_data: PrefixData = self._prefix_data
        reload_metas: dict = self._database.retrieve_last_saved_phone_metadatas()

        if self._skip_generation(reload_metas):
            terminate(DEBUG_VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"], 0)

        if DEV_CONFIG.FORCED_OPERATOR_CODES and DEV_CONFIG.UNSAFE:
            prefix_data.force_op_codes(DEV_CONFIG.FORCED_OPERATOR_CODES)
        else:
            if not DEV_CONFIG.DISABLE_SMART_RELOAD:
                self.__smart_reload(reload_metas, prefix_data)

        self.__do_generate(prefix_data, reload_metas)
        self._database.append_finite_collection_indicator()
        if DEV_CONFIG.DEBUG_MODE:
            print(DEBUG_VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])
