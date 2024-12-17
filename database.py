import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

this_file = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(this_file, "sql.db")

class SQL(tk.Tk):
    global db_file
    def __init__(self):
        super().__init__()
        self.geometry("250x250")
        self.title("SQL Projet CESI")
        self.resizable(width=False, height=False)
        self.default_widgets()
        if not os.path.exists(db_file):
            os.path.join(db_file)
            try:
                connexion = sqlite3.connect(db_file)
                connexion.execute("SELECT name FROM sqlite_master;")
                connexion.close()
            except sqlite3.DatabaseError:
                print(f"Le fichier '{db_file}' est corrompu. Suppression...")
                os.remove(db_file)
        self.sql_connexion()

    def default_widgets(self):
        self.clear()
        self.add_button = tk.Button(master=self, text="Ajouter une voiture", command=self.add_widgets).place(x=70, y=60)
        self.search_button = tk.Button(master=self, text="Rechercher une voiture", command=self.search_widgets).place(x=60, y=110)

    def add_widgets(self):
        self.clear()
        self.marque_label = tk.Label(master=self, text="Marque").place(x=105, y=10)
        self.marque_entry = tk.Entry(master=self)
        self.marque_entry.place(x=60, y=35)

        self.modele_label = tk.Label(master=self, text="Modèle").place(x=105, y=60)
        self.modele_entry = tk.Entry(master=self)
        self.modele_entry.place(x=60, y=85)

        self.annee_label = tk.Label(master=self, text="Année").place(x=105, y=110)
        self.annee_entry = tk.Entry(master=self)
        self.annee_entry.place(x=60, y=135)

        self.price_label = tk.Label(master=self, text="Prix (€)").place(x=110, y=160)
        self.price_entry = tk.Entry(master=self)
        self.price_entry.place(x=65, y=185)

        self.back_button = tk.Button(master=self, text="Retour", command=self.default_widgets).place(x=10, y=220)
        self.add_button = tk.Button(master=self, text="Ajouter", command=self.add_car).place(x=190, y=220)

    def search_widgets(self):
        self.clear()

        self.search_label = tk.Label(master=self, text="Rechercher").place(x=90, y=10)

        self.marque_label = tk.Label(master=self, text="Marque").place(x=10, y=40)
        self.marque_combo = ttk.Combobox(master=self, state="readonly")
        self.marque_combo.place(x=70, y=40)

        self.modele_label = tk.Label(master=self, text="Modèle").place(x=10, y=70)
        self.modele_combo = ttk.Combobox(master=self, state="readonly")
        self.modele_combo.place(x=70, y=70)

        self.annee_label = tk.Label(master=self, text="Année").place(x=10, y=100)
        self.annee_combo = ttk.Combobox(master=self, state="readonly")
        self.annee_combo.place(x=70, y=100)

        try:
            connexion = sqlite3.connect(db_file)
            cursor = connexion.cursor()
            cursor.execute("SELECT MIN(price), MAX(price) FROM voitures")
            min_price, max_price = cursor.fetchone()
            connexion.close()
            if min_price is None or max_price is None:
                min_price, max_price = 0, 1000000
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur avec la base de données : {e}")
            min_price, max_price = 0, 1000000

        self.price_label = tk.Label(master=self, text="Prix maximum").place(x=10, y=130)
        self.price_scale = tk.Scale(master=self, from_=min_price, to=max_price, orient="horizontal", length=200)
        self.price_scale.set(max_price / 2)
        self.price_scale.place(x=20, y=150)

        self.search_button = tk.Button(master=self, text="Rechercher", command=self.search_car).place(x=170, y=220)
        self.back_button = tk.Button(master=self, text="Retour", command=self.default_widgets).place(x=10, y=220)

        self.populate_comboboxes()

        self.marque_combo.bind("<<ComboboxSelected>>", lambda e: self.update_combobox(self.modele_combo, "modele", self.marque_combo, "marque"))
        self.marque_combo.bind("<<ComboboxSelected>>", lambda e: self.update_combobox(self.annee_combo, "annee", self.marque_combo, "marque"))
        self.modele_combo.bind("<<ComboboxSelected>>", lambda e: self.update_combobox(self.annee_combo, "annee", self.modele_combo, "modele"))
        self.marque_combo.bind("<<ComboboxSelected>>", lambda e: self.update_comboboxes_on_marque())
    def update_comboboxes_on_marque(self):
        selected_marque = self.marque_combo.get()
        self.update_combobox(self.modele_combo, "modele", self.marque_combo, "marque")
        self.update_combobox(self.annee_combo, "annee", self.marque_combo, "marque")

    def update_combobox(self, target_combobox, column, filter_combobox=None, filter_column=None):
        try:
            connexion = sqlite3.connect(db_file)
            cursor = connexion.cursor()

            query = f"SELECT DISTINCT {column} FROM voitures"
            params = []

            if filter_combobox and filter_column:
                selected_value = filter_combobox.get()
                if selected_value and selected_value != "TOUS":
                    query += f" WHERE {filter_column} = ?"
                    params.append(selected_value)

            cursor.execute(query, params)
            values = [row[0] for row in cursor.fetchall()]
            connexion.close()

            target_combobox['values'] = ["TOUS"] + sorted(values)
            target_combobox.current(0)

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur avec la base de données : {e}")


    def populate_comboboxes(self):
        try:
            connexion = sqlite3.connect(db_file)
            cursor = connexion.cursor()

            cursor.execute("SELECT DISTINCT marque FROM voitures")
            marques = [row[0] for row in cursor.fetchall()]
            self.marque_combo['values'] = ["TOUS"] + marques
            self.marque_combo.current(0)

            cursor.execute("SELECT DISTINCT modele FROM voitures")
            modeles = [row[0] for row in cursor.fetchall()]
            self.modele_combo['values'] = ["TOUS"] + modeles
            self.modele_combo.current(0)

            cursor.execute("SELECT DISTINCT annee FROM voitures")
            annees = [row[0] for row in cursor.fetchall()]
            self.annee_combo['values'] = ["TOUS"] + annees
            self.annee_combo.current(0)

            connexion.close()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur avec la base de données : {e}")

    def search_car(self):
        marque = self.marque_combo.get()
        modele = self.modele_combo.get()
        annee = self.annee_combo.get()
        max_price = self.price_scale.get()

        query = "SELECT * FROM voitures WHERE 1=1"
        params = []

        if marque != "TOUS":
            query += " AND marque = ?"
            params.append(marque)

        if modele != "TOUS":
            query += " AND modele = ?"
            params.append(modele)

        if annee != "TOUS":
            query += " AND annee = ?"
            params.append(annee)

        query += " AND price <= ?"
        params.append(max_price)

        try:
            connexion = sqlite3.connect(db_file)
            cursor = connexion.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            connexion.close()

            if results:
                result_text = "\n".join([f"Marque: {row[0]}, Modèle: {row[1]}, Année: {row[2]}, Prix: {row[3]}€" for row in results])
                messagebox.showinfo("Résultats", result_text)
            else:
                messagebox.showinfo("Résultats", "Aucune voiture trouvée.")

        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur avec la base de données : {e}")

    def clear(self):
        widgets = self.winfo_children()
        for widget in widgets:
            widget.destroy()

    def add_car(self):
        marque = self.marque_entry.get()
        modele = self.modele_entry.get()
        annee = self.annee_entry.get()
        price = self.price_entry.get()

        if not marque:
            messagebox.showerror("Erreur", "Marque requise")
        elif not marque.isalpha():
            messagebox.showerror("Erreur", "La marque doit contenir uniquement des lettres.")
        elif not modele:
            messagebox.showerror("Erreur", "Modèle requis")
        elif not annee:
            messagebox.showerror("Erreur", "Année requise")
        elif not annee.isdigit():
            messagebox.showerror("Erreur", "L'année doit contenir uniquement des chiffres.")
        elif not price:
            messagebox.showerror("Erreur", "Prix requis")
        elif not price.isdigit():
            messagebox.showerror("Erreur", "Le prix doit contenir uniquement des chiffres.")
        else:
            try:
                annee = int(annee)
                price = int(price)
                connexion = sqlite3.connect(db_file)
                cursor = connexion.cursor()

                cursor.execute("""
                    INSERT INTO voitures (marque, modele, annee, price)
                    VALUES (?, ?, ?, ?)
                """, (marque, modele, annee, price))
                connexion.commit()
                connexion.close()

                messagebox.showinfo("Succès", "Voiture ajoutée avec succès")
                self.default_widgets()

            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur avec la base de données : {e}")

    def sql_connexion(self):
        try:
            connexion = sqlite3.connect(db_file)
            cursor = connexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS voitures (
                    marque TEXT NOT NULL,
                    modele TEXT NOT NULL,
                    annee INTEGER NOT NULL,
                    price INTEGER NOT NULL
                )
            """)
            connexion.commit()
            print("Table 'voitures' créée avec succès ou déjà existante.")

        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion ou de la création de la table : {e}")


application = SQL()
application.mainloop()
