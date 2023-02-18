# coding: utf-8

from config.rules.generator import get_targeted_country
from metaprog.aliases import Void

def append_dynamic_conf(conf: dict) -> Void:
    country = get_targeted_country()
    db_table_name = country.lower()
    conf["MONGO_DB_TABLE"] = db_table_name
