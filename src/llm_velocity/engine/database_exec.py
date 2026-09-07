import sqlite3
import json
import threading
import time
from contextlib import contextmanager
from typing import  Callable
from src.llm_velocity.models.models import ChatContext
from src.llm_velocity.sql.queries import CREATE_TABLES
from pathlib import Path

class DatabaseExec:
    def __init__(self, database_file_path: Path, retry_count: int = 5):
        self.__db_file_path = database_file_path
        self.__ = retry_count
        self.__local = threading.local()

   
    
    def init_tables(self):
        with self.__transaction() as conn:
            conn.execute(CREATE_TABLES[0])
  
    def store_chat_context(self, chat_context: ChatContext):
        """ Method to store chat context into database """
        query = """INSERT INTO chat_context (user_message, llm_response) VALUES (?, ?);"""

        def run():
            with self.__transaction() as conn:   # use single underscore (recommended)
                cursor = conn.execute(
                    query,
                    (
                        chat_context.user_message,
                        json.dumps(chat_context.llm_response),
                    )
                )

                last_id = cursor.lastrowid
                cursor.close() 
                return last_id

        return self.__retry(run)
    
    # def get_all_chat_context(self):
    #     return self.__execute("SELECT * FROM chat_context;", fetch_all=True)
    
    def get_chat_context(self, chat_context_id: int) -> ChatContext :
        """ Method to fetch chat context by id from database """
        # print(chat_context_id + 1)

        query = "SELECT id, user_message, llm_response, created_at FROM chat_context WHERE id = ?; "

        result = self.__execute(query, (int(chat_context_id)+1,), fetch_one=True)

        return ChatContext(**self.__parse_json(result))
    
    def get_all_chat_user_message(self) -> list[str] :
        query = "SELECT user_message FROM chat_context; "

        result = self.__execute(query, fetch_all=True)

        return  [item["user_message"] for item in result]

######################### Private Methods ###############################   
    def __parse_json(self, row):
        if not row:
            return None
        if row.get("llm_response"):
            row["llm_response"] = json.loads(row["llm_response"])
        return row
    
    def __get_connection(self):
        if not hasattr(self.__local, "conn"):
            self.__local.conn = sqlite3.connect(
                self.__db_file_path,
                check_same_thread=False
            )
            self.__local.conn.row_factory = sqlite3.Row
        return self.__local.conn
    
    @contextmanager
    def __transaction(self):
        conn = self.__get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def __retry(self, func: Callable):
        for attempt in range(self.__):
            try:
                return func()
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < self.__ - 1:
                    time.sleep(0.1 * (attempt + 1))
                    continue
                raise

    def __execute(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
    ):
        def run():
            conn = self.__get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(query, params)

                if fetch_one:
                    row = cursor.fetchone()
                    return dict(row) if row else None

                if fetch_all:
                    rows = cursor.fetchall()
                    return [dict(r) for r in rows]

                return None

            finally:
                cursor.close()   # ✅ critical

        return self.__retry(run)