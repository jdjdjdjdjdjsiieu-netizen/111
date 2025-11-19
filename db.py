import sqlite3
from typing import Dict, Any, List, Tuple

DB_NAME = "alfa_bot.db"

def init_db():
    """Инициализация базы данных и создание таблиц."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            state TEXT NOT NULL DEFAULT 'start',
            context TEXT NOT NULL DEFAULT '{}'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            note TEXT,
            status TEXT NOT NULL DEFAULT 'new'
        )
    """)
    conn.commit()
    conn.close()

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Получение данных пользователя (состояние и контекст)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT state, context FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        import json
        return {"state": result[0], "context": json.loads(result[1])}
    return {"state": "start", "context": {}}

def update_user_data(user_id: int, state: str = None, context: Dict[str, Any] = None):
    """Обновление данных пользователя."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    current_data = get_user_data(user_id)
    
    new_state = state if state is not None else current_data["state"]
    new_context = context if context is not None else current_data["context"]
    
    import json
    context_json = json.dumps(new_context)

    cursor.execute("""
        INSERT INTO users (user_id, state, context) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET state = ?, context = ?
    """, (user_id, new_state, context_json, new_state, context_json))
    
    conn.commit()
    conn.close()

def add_contact(name: str, phone: str = None, note: str = None):
    """Добавление нового контакта в базу данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (name, phone, note) VALUES (?, ?, ?)
    """, (name, phone, note))
    conn.commit()
    conn.close()

def get_all_contacts() -> List[Tuple]:
    """Получение всех контактов."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, note, status FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_contact_by_id(contact_id: int) -> Dict[str, Any]:
    """Получение контакта по ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, note, status FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()
    conn.close()
    if contact:
        return {"id": contact[0], "name": contact[1], "phone": contact[2], "note": contact[3], "status": contact[4]}
    return None

def update_contact_status(contact_id: int, status: str):
    """Обновление статуса контакта."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET status = ? WHERE id = ?", (status, contact_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
