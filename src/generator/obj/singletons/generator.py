# coding: utf-8

from generator.obj.singletons.generator_base import GeneratorBase
from generator.metaprog.types import Void
from generator.sys.error import terminate
from generator.debug.logger import debug_logger as debug_logger
from generator.debug.vocab import VOCAB as DEBUG_VOCAB
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
import generator.smart_reload as smart_reload
import generator.phone_range_limit as limit

from typing import Optional, List
from generator.obj.contracts.prefix_data import PrefixData


class Generator(GeneratorBase):
    @staticmethod
    def _smart_reload(metadatas: Optional[dict], prefix_data: PrefixData) -> Void:
        smart_reload.slice_op_codes(metadatas, prefix_data)


    @staticmethod
    def _append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
        number_as_string: str = str(number)
        if number >= magnitude:
            return number_as_string
        number_len: int = len(number_as_string)
        number_of_zeros_to_append: int = abs(ndigits - number_len)
        phone_suffix: str = '0' * number_of_zeros_to_append + number_as_string
        return phone_suffix


    def _do_generate_range(self, r: range, block_len: int, magnitude: int, cur_op_code: str, country_code: str):
        prefix: str = country_code + cur_op_code

        for current_iteration in r:
            cur_phone_number_suffix: str = self._append_heading_zeros(
                current_iteration, block_len, magnitude)
            if not self._reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix):
                cur_phone_number: str = prefix + cur_phone_number_suffix
                self._database.save_phone_number(cur_phone_number, country_code,
                                    cur_op_code, cur_phone_number_suffix)
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_GENERATED_PHONE_NUMBERS:
                    debug_logger("GENERATED_PHONE_NUMBER", cur_phone_number)
            elif DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_PHONE_NUMBERS:
                cur_phone_number: str = prefix + cur_phone_number_suffix
                debug_logger("REJECTED_PHONE_NUMBER", cur_phone_number)


    def _do_generate_loop(self, country_code: str, op_codes: List[str], metadatas: Optional[dict]):
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
            self._do_generate_range(r, block_len, magnitude, cur_op_code, country_code)


    def _do_generate(self, prefix_data: PrefixData, metadatas: dict) -> Void:
        country_code: str = prefix_data.country_code()
        op_codes_a: List[str] = []
        op_codes_b: List[str] = []

        if prefix_data.start_with_desk():
            op_codes_a = prefix_data.operator_desk_codes()
            op_codes_b = prefix_data.operator_mobile_codes()
        else:
            op_codes_a = prefix_data.operator_mobile_codes()
            op_codes_b = prefix_data.operator_desk_codes()

        self._do_generate_loop(country_code, op_codes_a, metadatas)
        self._do_generate_loop(country_code, op_codes_b, metadatas)


    def process(self) -> Void:
        prefix_data: PrefixData = self._prefix_data
        reload_metas: dict = self._database.retrieve_last_saved_phone_metadatas()

        if self._skip_generation(reload_metas):
            terminate(DEBUG_VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"], 0)

        if DEV_CONFIG.FORCED_OPERATOR_CODES and DEV_CONFIG.UNSAFE:
            prefix_data.force_op_codes(DEV_CONFIG.FORCED_OPERATOR_CODES)
        else:
            if not DEV_CONFIG.DISABLE_SMART_RELOAD:
                self._smart_reload(reload_metas, prefix_data)

        self._do_generate(prefix_data, reload_metas)
        self._database.append_finite_collection_indicator()
        if DEV_CONFIG.DEBUG_MODE:
            print(DEBUG_VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])
