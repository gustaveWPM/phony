# coding: utf-8

from generator.config.rules.absolute_getters.generator import get_targeted_country
from generator.metaprog.aliases import Void

def append_dynamic_conf(conf: dict) -> Void:
    country = get_targeted_country()
    db_table_name = country.lower()
    conf["MONGO_DB_TABLE"] = db_table_name
