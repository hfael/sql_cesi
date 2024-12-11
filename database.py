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

def input_data():
    connection = sqlite3.connect("sql.db")
    cursor = connection.cursor()
    while True:
        data_input = input_data("> ")
        if data_input.lower() == "exit":
            break
        try:
            cursor.execute(data_input)
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("Requête envoyé avec succès.")
        except Exception as e:
            print(f"Erreur: {e}")
    connection.close()
    print("Déconnexion de la base de données")