import sqlite3
import json
import threading
import time
from contextlib import contextmanager
from typing import  Callable
from src.LLMVelocity.models.models import ChatContext
from src.LLMVelocity.sql.queries import CREATE_TABLES

class DatabaseExec:
    def __init__(self, database_name: str, retry_count: int = 5):
        self.__db_name = database_name
        self.__ = retry_count
        self.__local = threading.local()

   
    
    def init_tables(self):
        with self.__transaction() as conn:
            conn.execute(CREATE_TABLES[0])
  
    def store_chat_context(self, chat_context: ChatContext):
        """ Method to store chat context into database """
        query = """INSERT INTO chat_context (user_message, tool_name, llm_response)
            VALUES (?, ?, ?);"""

        def run():
            with self.__transaction() as conn:   # use single underscore (recommended)
                cursor = conn.execute(
                    query,
                    (
                        chat_context.user_message,
                        chat_context.tool_name.strip(),
                        json.dumps(chat_context.llm_response)
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
        print(chat_context_id + 1)

        query = "SELECT id, user_message, tool_name, llm_response, created_at FROM chat_context WHERE id = ?; "

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
                self.__db_name,
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
            print("QUERY:", query)
            print("PARAMS:", params)


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












####################### postgresql ########################

# # from psycopg_pool import ConnectionPool
# # from psycopg import Error
# # from psycopg.errors import UniqueViolation
# import sqlite3
# from src.LLMVelocity.models.models import ChatContext
# from src.LLMVelocity.constants import constants
# from src.LLMVelocity.sql.queries import CREATE_TABLES

# class DatabaseExec:

#     # **to connect to postgresql
#     def __init__(self, conn_str: str):
#         self.__db_pool = ConnectionPool(
#             conninfo=conn_str, min_size=5, max_size=20, timeout=10
#         )

#     def __execute_query(self, query: str, params=None, fetch_one=False, fetch_all=False):
#         """ Generic method to execute queries safely """
#         try:
#             with self.__db_pool.connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute(query, params, prepare=True)

#                     if fetch_one:
#                         return cur.fetchone()

#                     if fetch_all:
#                         return cur.fetchall()

#                     conn.commit()
#                     return True

#         # 🔹 Specific DB Errors
#         except UniqueViolation as e:
#             print(f"Unique constraint error: {e}")
#             return {"error": "duplicate_entry"}

#         # 🔹 Generic Psycopg Error
#         except Error as e:
#             print(f"Database error: {e}")
#             return {"error": "database_error"}

#         # 🔹 Any unexpected error
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             return {"error": "unknown_error_while_query_execution"}

#     def store_chat_context(self, chat_context: ChatContext):
#         """ Method to store chat context into database """
      
#         query = """
#             INSERT INTO chat_context (user_message, tool_name, llm_response)
#             VALUES (%s, %s, %s)
#             RETURNING id;
#             """
   
#         result = self.__execute_query(query, (chat_context.user_message, chat_context.tool_name, chat_context.llm_response), fetch_one=True)
   
#         if isinstance(result, dict) and "error" in result:
#             return result
  
#         return {"id": result[0]}
    
#     def get_chat_context(self, chat_context_id: int):
#         """ Method to fetch chat context by id from database """

#         query = """
#             SELECT id, user_message, tool_name, llm_response, created_at
#             FROM chat_context
#             WHERE id = %s;
#             """

#         return self.__execute_query(query, (chat_context_id,), fetch_one=True)


#     def delete_interaction(self, chat_context_id: int):
#         """ Method to fetch chat context by id from database """
#         query = """
#             DELETE FROM chat_context
#             WHERE id = %s
#             """
#         return self.__execute_query(query, (chat_context_id,), fetch_one=True)