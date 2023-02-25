# coding: utf-8


from generator.metaprog.singleton import Singleton
from generator.obj.implementations.prefix_data import PrefixData
from generator.obj.implementations.singletons.database import Database
import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
from generator.config.rules.generator import GENERATOR as GENERATOR_CONFIG
from generator.debug.logger import debug_logger
from generator.metaprog.types import Void


import random
from typing import List, Optional, Tuple


class Decks(metaclass=Singleton):
    def __init__(self, prefix_data: PrefixData, db: Database, start_with_desk: bool):
        self._deck_a: List[str] = []
        self._deck_b: List[str] = []
        self.__banned_op_codes: List[str] = GENERATOR_CONFIG["BANNED_OPERATOR_CODES"]
        self.__disable_shuffle = DEV_CONFIG.DISABLE_SHUFFLE
        self.__database = db
        self.__build_decks(prefix_data, start_with_desk)


    def __do_eject_duplicates(self, collection) -> Void:
        roll_again = False
        for card_label_a in collection:
            for card_label_b in collection:
                if card_label_a == card_label_b:
                    continue
                if card_label_a.startswith(card_label_b):
                    if DEBUGGER_CONFIG.PRINT_DUPLICATES_KILLER_LOGS:
                        debug_logger("KEPT_OPERATOR_CODE", card_label_b)
                        debug_logger("REMOVED_OPERATOR_CODE", card_label_a)
                    collection.remove(card_label_a)
                elif card_label_b.startswith(card_label_a):
                    if DEBUGGER_CONFIG.PRINT_DUPLICATES_KILLER_LOGS:
                        debug_logger("KEPT_OPERATOR_CODE", card_label_a)
                        debug_logger("REMOVED_OPERATOR_CODE", card_label_b)
                    collection.remove(card_label_b)
                    roll_again = True
            if roll_again:
                break
        if roll_again:
            self.__do_eject_duplicates(collection)


    def __eject_duplicates(self) -> Void:
        self.__do_eject_duplicates(self._deck_a)
        self.__do_eject_duplicates(self._deck_b)


    def __eject_banned_cards(self) -> Void:
        for banned_code in self.__banned_op_codes:
            for card_label in self._deck_a:
                if card_label.startswith(banned_code):
                    self._deck_a.remove(card_label)
            for card_label in self._deck_b:
                if card_label.startswith(banned_code):
                    self._deck_b.remove(card_label)


    def __build_decks(self, prefix_data: PrefixData, start_with_desk: bool) -> Void:
        if start_with_desk:
            self._deck_a = prefix_data.operator_desk_codes()
            self._deck_b = prefix_data.operator_mobile_codes()
        else:
            self._deck_a = prefix_data.operator_mobile_codes()
            self._deck_b = prefix_data.operator_desk_codes()
        self.__eject_banned_cards()
        self.__eject_duplicates()


    def __do_random_pick(self, collection: List[str]) -> int:
        if self.__disable_shuffle:
            return collection[0]
        return random.choice(collection)


    def __eject_card(self, card_label: str) -> Void:
        if card_label in self._deck_a:
            self._deck_a.remove(card_label)
        else:
            self._deck_b.remove(card_label)


    def __skip_op_code_range_generation(self, data: Optional[dict]) -> bool:
        if data is None:
            return False
        return self.__database.is_finite_op_code_range(data)


    def __should_pick_again(self, reject_datas: dict, operator_code_picked: str) -> bool:
        if self.__skip_op_code_range_generation(reject_datas):
            if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_SKIPPED_OPERATOR_CODES:
                debug_logger("SKIPPED_OPERATOR_CODE", operator_code_picked)
        else:
            return False
        return True


    def pick_in_deck(self) -> Tuple[Optional[str], dict]:
        pick_again = True
        while pick_again:
            if self._deck_a != []:
                operator_code_picked = self.__do_random_pick(self._deck_a)
            elif self._deck_b != []:
                operator_code_picked = self.__do_random_pick(self._deck_b)
            else:
                return None

            reject_datas: dict = self.__database._retrieve_op_code_range_finite_indicator(operator_code_picked)
            pick_again = self.__should_pick_again(reject_datas, operator_code_picked)

            if pick_again:
                self.__eject_card(operator_code_picked)
            else:
                metadatas: dict = self.__database._retrieve_last_phone_number_entry_with_op_code(operator_code_picked)
                return operator_code_picked, metadatas
