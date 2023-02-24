# coding: utf-8


from generator.debug.vocab import VOCAB as DEBUG_VOCAB
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
from generator.debug.logger import debug_logger
from generator.obj.implementations.prefix_data import PrefixData
from generator.obj.implementations.database_entry import DatabaseEntry
from generator.obj.implementations.singletons.generator_base import GeneratorBase
from generator.sys.error import terminate
import generator.phone_range_limit as limit
from generator.metaprog.types import Void

from typing import Optional, List


class Generator(GeneratorBase):
    @staticmethod
    def __append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
        number_as_string = str(number)
        if number >= magnitude:
            return number_as_string
        number_len = len(number_as_string)
        number_of_zeros_to_append = abs(ndigits - number_len)
        phone_suffix = '0' * number_of_zeros_to_append + number_as_string
        return phone_suffix


    def __start_with_desk(self, value: Optional[bool] = None) -> Optional[bool]:
        if value is None:
            return self._start_with_desk
        self._start_with_desk = value


    def __do_generate_range(self, r: range, block_len: int, magnitude: int, cur_op_code: str, country_code: str):
        prefix: str = country_code + cur_op_code
        last_iteration = r[-1]
        db_entries_counter = 0
        db_entries_chunk: List[DatabaseEntry] = []

        for current_iteration in r:
            cur_phone_number_suffix: str = self.__append_heading_zeros(current_iteration, block_len, magnitude)
            cur_phone_number = prefix + cur_phone_number_suffix

            if not self._reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix):
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_GENERATED_PHONE_NUMBERS:
                    debug_logger("GENERATED_PHONE_NUMBER", f"{cur_phone_number} ; op_code: {cur_op_code}")

                if self._database._disabled_persistence:
                    continue

                database_entry: DatabaseEntry = DatabaseEntry(cur_phone_number, country_code, cur_op_code, cur_phone_number_suffix)

                db_entries_chunk.append(database_entry)
                db_entries_counter += 1
                if db_entries_counter >= DEV_CONFIG.DB_ENTRIES_CHUNK_SIZE:
                    self._database.save_phone_numbers(db_entries_chunk)
                    db_entries_chunk = []
                    db_entries_counter = 0

            elif DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_PHONE_NUMBERS:
                debug_logger("REJECTED_PHONE_NUMBER", cur_phone_number)

            if current_iteration == last_iteration:
                if db_entries_counter > 0:
                    self._database.save_phone_numbers(db_entries_chunk)
                self._database.append_finite_op_code_range_indicator(cur_op_code)

    # * ... Fixes potential issues related to the smart reload feature, terminates if invalid unsafe params.
    @staticmethod
    def __sanitized_range(range_start: int, range_end: int) -> range:
        if range_start < 0:
            terminate("Invalid range start value.")
        elif range_end < 0:
            terminate("Invalid range end value.")
        if range_end < range_start:
            range_end = range_start
        if range_start == range_end:
            if range_start == 0:
                range_end = 1
            else:
                range_start -= 1

        r = range(range_start, range_end)
        return r


    def __do_generate_loop(self, country_code: str, op_codes: List[str], metadatas: Optional[dict]):
        for cur_op_code in op_codes:
            if self._is_banned_op_code(cur_op_code):
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_OPERATOR_CODES:
                    debug_logger("REJECTED_OPERATOR_CODE", cur_op_code)
                continue

            reload_metas: dict = self._database._retrieve_last_phone_number_entry_with_op_code(cur_op_code)
            if self._skip_op_code_range_generation(reload_metas):
                continue

            block_len: int = limit.compute_range_len(cur_op_code)
            magnitude: int = 10 ** (block_len - 1)
            range_end: int = limit.compute_range_end(cur_op_code)
            range_start: int = limit.compute_range_start(metadatas, cur_op_code, magnitude)
            r = self.__sanitized_range(range_start, range_end)
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
            index = operator_desk_codes.index(needle)
            prefix_data.operator_desk_codes(operator_desk_codes[index:])
            self.__start_with_desk(True)

        if needle in operator_mobile_codes:
            index = operator_mobile_codes.index(needle)
            prefix_data.operator_mobile_codes(operator_mobile_codes[index:])
            self.__start_with_desk(False)


    def __smart_reload(self, metadatas: Optional[dict], prefix_data: PrefixData) -> Void:
        self.__slice_op_codes(metadatas, prefix_data)


    def process(self) -> Void:
        prefix_data = self._prefix_data
        reload_metas = self._database.retrieve_last_saved_phone_metadatas()

        if self._skip_whole_generation(reload_metas):
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
