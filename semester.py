#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# semester.py

# Importiere notwendige Module und Klassen
from dbzugriff import DBZugriff  # Klasse zur Verwaltung der Datenbankzugriffe
from modul import Modul          # Import für Modul

class Semester:
    """
    Repräsentiert ein Semester mit zugehörigen Modulen.
    """
    def __init__(self, semester_code: str, semester_name: str):
        """
        Initialisiert ein Semester-Objekt.

        :param semester_code: Eindeutiger Code des Semesters.
        :param semester_name: Name des Semesters.
        """
        self.semester_code = semester_code
        self.semester_name = semester_name

    def __str__(self):
        """
        Gibt eine String-Repräsentation des Semesters zurück.

        :return: Eine formatierte Zeichenkette mit Semestername und Code.
        """
        return f"Semester: {self.semester_name} (Code: {self.semester_code})"

    def load_moduls(self, db_handler: DBZugriff):
        """
        Lädt und gibt die Module zurück, die diesem Semester zugeordnet sind.
        :param db_handler: Instanz von DBZugriff, um Daten zu laden
        :return: Liste von Modul-Objekten
        """
        # Daten aus der semester_modul.csv laden
        semester_modul_data = db_handler.get_semester_modul()
        
        # Die Modulkodes, die diesem Semester zugeordnet sind
        modul_codes = semester_modul_data[semester_modul_data["semester_code"] == self.semester_code]["modul_code"]
        
        # Für jedes Modul einen Modul-Objekt erstellen
        module = [Modul(modul_code) for modul_code in modul_codes]
        return module

    def show_modul(self, db_handler: DBZugriff):
        """
        Zeigt die Module des Semesters an.
        :param db_handler: Instanz von DBZugriff
        """
        module = self.load_moduls(db_handler)
        for modul in module:
            print(modul)

