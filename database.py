import sqlite3
import os

this_file = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(this_file, "sql.db")

def new_db():
    """Créer la base de données et la table si elles n'existent pas."""
    if os.path.exists(db_file):
        try:
            connection = sqlite3.connect(db_file)
            connection.execute("SELECT name FROM sqlite_master;")
            connection.close()
        except sqlite3.DatabaseError:
            print(f"Le fichier '{db_file}' est corrompu. Suppression...")
            os.remove(db_file)

    connection = sqlite3.connect(db_file)
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
    print("Création de la base de données terminée.")

def insert_data():
    """Insérer des données par défaut dans la base."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO content (critere1, critere2, critere3) 
        VALUES (?, ?, ?)
    """, [
        ("Voyage", "Train", "France"),
        ("Aventure", "Randonnée", "Alpes"),
        ("Nature", "Vélo", "Pays-Bas"),
        ("Plage", "Voiture", "Espagne"),
        ("Cuisine", "Recettes", "Thaïlande"),
    ])
    conn.commit()
    conn.close()
    print("Données par défaut insérées avec succès.")

def sql_input():
    """Permet d'exécuter des requêtes SQL saisies par l'utilisateur."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    print("Tapez vos requêtes SQL (tapez 'back' pour revenir au menu principal).")
    while True:
        query = input("SQL > ")
        if query.lower() == "back":
            print("Retour au menu principal.")
            break
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("Requête exécutée avec succès.")
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur : {e}")
    conn.close()

def main_menu():
    """Afficher le menu principal et gérer les choix."""
    while True:
        print("\nOptions disponibles :")
        print("1. Création de la base de données")
        print("2. Insérer des données de base")
        print("3. Faire des requêtes SQL")
        print("4. Quitter")
        choice = input("> ")
        if choice == "1":
            new_db()
        elif choice == "2":
            insert_data()
        elif choice == "3":
            sql_input()
        elif choice == "4":
            print("Au revoir !")
            break
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main_menu()
