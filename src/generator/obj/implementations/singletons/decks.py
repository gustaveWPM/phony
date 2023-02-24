# coding: utf-8


from generator.metaprog.singleton import Singleton
from generator.obj.implementations.prefix_data import PrefixData
import generator.config.rules.dev.generator as DEV_CONFIG


from typing import List, Optional


class Decks(metaclass=Singleton):
    def __init__(self, prefix_data: PrefixData, start_with_desk: bool):
        self.__disable_shuffle = DEV_CONFIG.DISABLE_SHUFFLE
        self._deck_a: List[str] = []
        self._deck_b: List[str] = []
        self.__build_decks(prefix_data, start_with_desk)


    def __build_decks(self, prefix_data: PrefixData, start_with_desk: bool):
        if start_with_desk:
            self._deck_a = prefix_data.operator_desk_codes()
            self._deck_b = prefix_data.operator_mobile_codes()
        else:
            self._deck_a = prefix_data.operator_mobile_codes()
            self._deck_b = prefix_data.operator_desk_codes()


    def pick_in_deck(self) -> Optional[str]:
        pick_again = False
        if self._deck_a != []:
            pass
        elif self._deck_b != []:
            pass
        else:
            return None

        if pick_again:
            return self.pick_in_deck()
