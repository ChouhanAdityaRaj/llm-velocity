CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS chat_context (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT NOT NULL,
        tool_name TEXT,
        llm_response TEXT NOT NULL,
        created_at INTEGER DEFAULT (strftime('%s', 'now'))
    )
    """
]