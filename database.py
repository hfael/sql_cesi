import sqlite3

def new_db():
    connection = sqlite3.connect("sql.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            critere1 TEXT NOT NULL,
            critere2 TEXT,
            critere3 TEXT
        )
    """)
    connection.commit()
    connection.close()
    print("Création de la base de données fini.")