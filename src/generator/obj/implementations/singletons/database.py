# coding: utf-8


import generator.config.rules.dev.generator as DEV_CONFIG
import generator.config.rules.dev.debugger as DEBUGGER_CONFIG
from generator.config.rules.dev.database import DB as DATABASE_CONFIG
from generator.debug.logger import debug_logger
from generator.config.builders.database import append_dynamic_conf as build_config
from generator.obj.implementations.database_entry import DatabaseEntry
from generator.metaprog.singleton import Singleton
from generator.metaprog.types import Void


import pymongo
from pymongo.collection import Collection as DatabaseCollection
from multiprocessing.pool import ThreadPool
from typing import Optional, List


class Database(metaclass=Singleton):
    def __init__(self):
        def index_database(self) -> Void:
            db_table: DatabaseCollection = self._get_db_table()
            db_table.create_index([ ("phone_number", pymongo.ASCENDING) ])


        def initialize(self) -> Void:
            build_config(DATABASE_CONFIG)
            self._mongo_client = pymongo.MongoClient(DATABASE_CONFIG["MONGO_DB_CONNECTION_URI"])
            self._db_name_key = DATABASE_CONFIG["MONGO_DB_NAME"]
            self._db = self._mongo_client[self._db_name_key]
            self._db_table_key = DATABASE_CONFIG["MONGO_DB_TABLE"]
            index_database(self)


        initialize(self)


    @staticmethod
    def is_finite_collection(data: dict) -> bool:
        for key in data:
            if data[key] != "-1":
                return False
        return True


    @staticmethod
    def is_finite_op_code_range(data: dict) -> bool:
        for key in data:
            if data[key] == "-1":
                return True
        return False


    def _get_db_table(self) -> DatabaseCollection:
        return self._db[self._db_table_key]


    def _retrieve_last_saved_phone_number_entry(self) -> Optional[dict]:
        db_table: DatabaseCollection = self._get_db_table()
        try:
            d: dict = db_table.find_one('_id', pymongo.DESCENDING)
            return d
        except:
            return None


    def _retrieve_last_phone_number_entry_with_op_code(self, op_code: str) -> Optional[dict]:
        db_table: DatabaseCollection = self._get_db_table()
        try:
            d: dict = db_table.find({"operator_code": op_code}).sort("phone_number", pymongo.DESCENDING).limit(1)[0]
            return d
        except:
            return None


    def _retrieve_op_code_range_finite_indicator(self, op_code: str) -> Optional[dict]:
        db_table: DatabaseCollection = self._get_db_table()
        try:
            d: dict = db_table.find_one({"operator_code": op_code, "phone_number": "-1"})
            return d
        except:
            return None


    def __save_phone_number(*args) -> Void:
        self_instance, database_entry = args
        db_table: DatabaseCollection = self_instance._get_db_table()
        entry_schema: dict = database_entry.schema()

        if DEV_CONFIG.ALLOW_DUPLICATES:
            db_table.insert_one(entry_schema)
        else:
            db_table.update_one({"phone_number": entry_schema["phone_number"]}, {
                                 "$set": entry_schema}, upsert=True)


    def __weak_save_phone_numbers(self, db_entries: List[DatabaseEntry]) -> Void:
        entries: dict = [entry.schema() for entry in db_entries]
        db_table: DatabaseCollection = self._get_db_table()
        db_table.insert_many(entries)


    def save_phone_numbers(self, entries: List[DatabaseEntry], force_disable_multithreading = False) -> Void:
        if DEV_CONFIG.ALLOW_DUPLICATES:
            self.__weak_save_phone_numbers(entries)

        elif DEV_CONFIG.DISABLE_MULTITHREADING or force_disable_multithreading:
            for database_entry in entries:
                self.__save_phone_number(database_entry)

        else:
            with ThreadPool() as pool:
                pool.map(self.__save_phone_number, entries)

        if DEV_CONFIG.DEBUG_MODE and DEBUGGER_CONFIG.PRINT_DB_UPDATES:
            debug_logger("SAVED_CHUNK_IN_DATABASE")


    def retrieve_last_saved_phone_metadatas(self) -> Optional[dict]:
        entry: Optional[dict] = self._retrieve_last_saved_phone_number_entry()
        if entry is None:
            return None
        return entry


    def append_finite_collection_indicator(self) -> Void:
        db_entry = DatabaseEntry("-1", "-1", "-1", "-1")
        self.__save_phone_number(db_entry)


    def append_finite_op_code_range_indicator(self, op_code: str) -> Void:
        db_entry = DatabaseEntry("-1", "-1", op_code, "-1")
        self.__save_phone_number(db_entry)
