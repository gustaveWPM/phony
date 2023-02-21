# coding: utf-8


from generator.obj.implementations.singletons.generator import Generator
from generator.metaprog.types import Void


def run() -> Void:
    generator = Generator()
    generator.process()
