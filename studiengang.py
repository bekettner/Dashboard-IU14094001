#!/usr/bin/env python
# coding: utf-8

# In[6]:


# studiengang.py

# Importiere notwendige Module und Klassen
from dbzugriff import DBZugriff # Klasse zur Verwaltung der Datenbankzugriffe
from semester import Semester # Import von Semestern

class Studiengang:
    """
    Repräsentiert einen Studiengang mit zugehörigen Eigenschaften und Methoden zur Verwaltung der Semester.
    """
    def __init__(self, studiengang_code: str, studiengang_name: str, erforderliche_credits: int, mindeststudienzeit: int):
        """
        Initialisiert ein Studiengang-Objekt.

        :param studiengang_code: Eindeutiger Code des Studiengangs.
        :param studiengang_name: Name des Studiengangs.
        :param erforderliche_credits: Erforderliche Credits zum Abschluss des Studiengangs.
        :param mindeststudienzeit: Mindestanzahl der Semester für den Abschluss.
        """
        self.studiengang_code = studiengang_code
        self.studiengang_name = studiengang_name
        self.erforderliche_credits = erforderliche_credits
        self.mindeststudienzeit = mindeststudienzeit

    def get_semester(self, dbzugriff: DBZugriff):
        """
        Lädt alle Semester des Studiengangs und gibt sie als Liste von Semester-Objekten zurück.

        :param dbzugriff: Instanz von DBZugriff, um auf die Semester-Daten zuzugreifen.
        :return: Liste von Semester-Objekten.
        """
        semester_list = []
        
        # Hole die Semester-Daten für den Studiengang über DBZugriff
        studiengang_semester_daten = dbzugriff.get_studiengang_semester(self.studiengang_code)
        
        if studiengang_semester_daten is not None:
            for index, semester_info in studiengang_semester_daten.iterrows():
                semester_code = semester_info["semester_code"]
                semester_name = semester_info["semester_name"]
                semester = Semester(semester_code, semester_name)
                
                # Lade die Module für dieses Semester
                semester.load_moduls(dbzugriff)  # Methode zum Laden der Module für das Semester
                
                # Füge das Semester zur Liste hinzu
                semester_list.append(semester)
        
        return semester_list

    def __str__(self):
        """
        Gibt eine String-Darstellung des Studiengangs zurück.

        :return: Formatierte Zeichenkette mit Informationen zum Studiengang.
        """
        return (
            f"Studiengang: {self.studiengang_name} (Code: {self.studiengang_code})\n"
            f"Erforderliche Credits: {self.erforderliche_credits}\n"
            f"Mindeststudienzeit: {self.mindeststudienzeit} Semester"
        )


# In[ ]:




