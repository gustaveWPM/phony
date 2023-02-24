# coding: utf-8


from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
import generator.config.builders.generator as generator_config_builder
import generator.config.validator as config_validator
from generator.obj.implementations.prefix_data import PrefixData
from generator.obj.implementations.singletons.database import Database
from generator.metaprog.singleton import Singleton


from typing import Optional, List


class GeneratorBase(metaclass=Singleton):
    def __init__(self):
        self._database = Database()
        generator_config_builder.append_dynamic_conf(GENERATOR_CONFIG)
        self._target = GENERATOR_CONFIG["TARGET"]
        self._ndigits = GENERATOR_CONFIG["NDIGITS"]
        self._same_digit_threshold: int = GENERATOR_CONFIG["SAME_DIGIT_THRESHOLD"]
        self._consecutive_same_digit_threshold: int = GENERATOR_CONFIG["CONSECUTIVE_SAME_DIGIT_THRESHOLD"]
        self._last_block_head_max_zeros: int = GENERATOR_CONFIG["LAST_BLOCK_HEAD_MAX_ZEROS"]
        self._banned_op_codes: List[str] = GENERATOR_CONFIG["BANNED_OPERATOR_CODES"]
        self._prefix_data: PrefixData = GENERATOR_CONFIG["PREFIX_DATA"]
        self._start_with_desk: bool = GENERATOR_CONFIG["START_WITH_DESK_OPERATOR_CODES"]
        config_validator.check_config(GENERATOR_CONFIG)


    def _is_banned_op_code(self, op_code: str) -> bool:
        for cur_banned_op_code in self._banned_op_codes:
            if op_code == cur_banned_op_code:
                return True
        return False


    def _reject_phone_number_suffix(self, op_code: str, phone_number_suffix: str) -> bool:
        digits = "0123456789"
        banned_pattern = '0' * (self._last_block_head_max_zeros + 1)
        whole_phone_number: str = op_code + phone_number_suffix

        if phone_number_suffix.startswith(banned_pattern):
            return True

        for banned_pattern in self._banned_op_codes:
            if banned_pattern == '':
                break
            if whole_phone_number.startswith(banned_pattern):
                return True

        for digit in digits:
            if whole_phone_number.count(digit) > self._same_digit_threshold:
                return True
            if self._consecutive_same_digit_threshold > 0:
                banned_pattern: str = digit * (self._consecutive_same_digit_threshold + 1)
                if banned_pattern in whole_phone_number:
                    return True
        return False


    def _skip_generation(self, data: Optional[dict]) -> bool:
        if data is None:
            return False
        return self._database.is_finite_collection(data)
