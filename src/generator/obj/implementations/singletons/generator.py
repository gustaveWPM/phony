# coding: utf-8


from generator.debug.vocab import VOCAB as DEBUG_VOCAB
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
from generator.debug.logger import debug_logger
from generator.obj.implementations.prefix_data import PrefixData
from generator.obj.implementations.database_entry import DatabaseEntry
from generator.obj.implementations.singletons.generator_base import GeneratorBase
from generator.obj.implementations.singletons.decks import Decks

from generator.sys.error import terminate
import generator.phone_range_limit as limit
from generator.metaprog.types import Void

from typing import List
import random


class Generator(GeneratorBase):
    def __init__(self):
        super().__init__()
        if DEV_CONFIG.FORCED_OPERATOR_CODES and DEV_CONFIG.UNSAFE:
            self._prefix_data.force_operator_codes(DEV_CONFIG.FORCED_OPERATOR_CODES)
        self._decks = Decks(self._prefix_data, self._database, self._start_with_landline)


    @staticmethod
    def __append_heading_zeros(number: int, ndigits: int, magnitude: int) -> str:
        number_as_string = str(number)
        if number >= magnitude:
            return number_as_string
        number_len = len(number_as_string)
        number_of_zeros_to_append = abs(ndigits - number_len)
        phone_suffix = '0' * number_of_zeros_to_append + number_as_string
        return phone_suffix


    @staticmethod
    def __compute_db_entries_counter_max():
        db_entries_counter_max = DEV_CONFIG.DB_ENTRIES_CHUNK_SIZE
        if DEV_CONFIG.DB_ENTRIES_CHUNK_SIZE_RANDOM_DELTA > 0:
            db_entries_counter_max -= random.randint(0, DEV_CONFIG.DB_ENTRIES_CHUNK_SIZE_RANDOM_DELTA)
        return db_entries_counter_max


    def __do_generate_range(self, r: range, block_len: int, magnitude: int, cur_op_code: str, country_code: str):
        prefix: str = country_code + cur_op_code
        db_entries_chunk: List[DatabaseEntry] = []
        last_iteration = r[-1]
        db_entries_counter = 0
        db_entries_counter_max = self.__compute_db_entries_counter_max()
        db_chunks_counter = 0
        db_chunks_counter_max = DEV_CONFIG.MAX_DB_CHUNKS_RECORDS_BEFORE_SHUFFLE

        for current_iteration in r:
            cur_phone_number_suffix: str = self.__append_heading_zeros(current_iteration, block_len, magnitude)
            cur_phone_number = prefix + cur_phone_number_suffix

            if not self._reject_phone_number_suffix(cur_op_code, cur_phone_number_suffix):
                if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_GENERATED_PHONE_NUMBERS:
                    debug_logger("GENERATED_PHONE_NUMBER", f"{cur_phone_number} ; op_code: {cur_op_code}")

                database_entry: DatabaseEntry = DatabaseEntry(cur_phone_number, country_code, cur_op_code, cur_phone_number_suffix)
                db_entries_chunk.append(database_entry)
                db_entries_counter += 1
                if db_entries_counter >= db_entries_counter_max:
                    self._database.save_phone_numbers(db_entries_chunk)
                    db_entries_chunk = []
                    db_chunks_counter += 1
                    db_entries_counter = 0
                    db_entries_counter_max = self.__compute_db_entries_counter_max()
                    if not DEV_CONFIG.DISABLE_SHUFFLE and db_chunks_counter_max > 0 and db_chunks_counter >= db_chunks_counter_max:
                        break

            elif DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_REJECTED_PHONE_NUMBERS:
                debug_logger("REJECTED_PHONE_NUMBER", cur_phone_number)

            if current_iteration == last_iteration:
                if db_entries_counter > 0:
                    self._database.save_phone_numbers(db_entries_chunk)
                self._database.append_finite_op_code_range_indicator(cur_op_code)


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


    def __do_generate(self, prefix_data: PrefixData) -> Void:
        country_code: str = prefix_data.country_code()
        picked_op_code, metadatas = self._decks.pick_in_deck()
        while picked_op_code:
            block_len: int = limit.compute_range_len(picked_op_code)
            magnitude: int = 10 ** (block_len - 1)
            range_end: int = limit.compute_range_end(picked_op_code)
            range_start: int = limit.compute_range_start(metadatas, picked_op_code, magnitude)
            r = self.__sanitized_range(range_start, range_end)
            self.__do_generate_range(r, block_len, magnitude, picked_op_code, country_code)
            picked_op_code, metadatas = self._decks.pick_in_deck()


    def process(self) -> Void:
        prefix_data = self._prefix_data
        reload_metas = self._database.retrieve_last_saved_phone_metadatas()

        if self._skip_whole_generation(reload_metas):
            terminate(DEBUG_VOCAB["WARNING_MSG"]["ALREADY_REACHED_FINAL_EXIT_POINT"], 0)

        self.__do_generate(prefix_data)
        self._database.append_finite_collection_indicator()
        if DEV_CONFIG.DEBUG_MODE:
            print(DEBUG_VOCAB["SUCCESS_MSG"]["REACHED_FINAL_EXIT_POINT"])
