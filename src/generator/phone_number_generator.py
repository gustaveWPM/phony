# coding: utf-8

from generator.metaprog.types import Void
from generator.obj.implementations.singletons.generator import Generator

def run() -> Void:
    generator = Generator()
    generator.process()
