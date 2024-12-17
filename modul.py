#!/usr/bin/env python
# coding: utf-8

# In[2]:


# modul.py

# Importiere notwendige Module und Klassen
from dbzugriff import DBZugriff # Klasse zur Verwaltung der Datenbankzugriffe

class Modul:
    """
    Repräsentiert ein Modul, das in einem Studiengang angeboten wird. 
    Diese Klasse lädt und speichert die relevanten Daten eines Moduls.
    """
    def __init__(self, modul_code: str, modul_name: str, credits: int, tutor: str, preufungsform: str, db_handler: DBZugriff):
        """
        Initialisiert die Modul-Klasse und lädt die Daten des Moduls aus der Datenbank.

        :param modul_code: Der eindeutige Code des Moduls.
        :param modul_name: Der Name des Moduls.
        :param credits: Die Anzahl der ECTS-Credits, die für das Modul vergeben werden.
        :param tutor: Der Tutor, der für das Modul verantwortlich ist.
        :param pruefungsform: Die Prüfungsform des Moduls (z. B. Klausur, Hausarbeit).
        :param db_handler: Eine Instanz der DBZugriff-Klasse für den Zugriff auf die Datenbank.
        """
        self.modul_code = modul_code
        self.modul_name = modul_name
        self.credits = credits
        self.tutor = tutor
        self.pruefungsform = pruefungsform
        self.db_handler = db_handler
        
        # Lade die Moduldaten sofort beim Erstellen des Moduls
        self.lade_daten()

    def lade_daten(self):
        """
        Lädt die Moduldaten aus der Datenbank anhand des modul_code. 

        Aktualisiert die Attribute des Objekts mit den geladenen Daten.
        Falls keine Daten gefunden werden, wird ein Fehler ausgegeben.
        """
        try:
            # Hole die Daten des Moduls basierend auf modul_code
            modul_data = self.db_handler.get_modul(self.modul_code)
            
            # Überprüfen, ob Daten gefunden wurden
            if modul_data is not None:
                # Aktualisiere die Attribute mit den geladenen Werten
                self.modul_name = modul_data["modul_name"]  # Name des Moduls
                self.credits = modul_data["credits"]       # Credits des Moduls
                self.tutor = modul_data["tutor"]           # Tutor des Moduls
                self.pruefungsform = modul_data["pruefungsform"]  # Prüfungsform
            else:
                raise ValueError(f"Modul {self.modul_code} konnte nicht gefunden werden.")
        except KeyError as e:
            print(f"Fehler beim Zugriff auf die Moduldaten: {e}")
        except Exception as e:
            print(f"Unerwarteter Fehler beim Laden der Moduldaten: {e}")

    def __str__(self):
        """
        Gibt eine textuelle Darstellung des Moduls zurück.

        :return: Eine formatierte Zeichenkette mit den Moduldaten.
        """
        if self.modul_name is None:
            return f"Modul mit Code {self.modul_code} wurde noch nicht geladen."
        return (f"Modul: {self.modul_name} (Code: {self.modul_code}), "
                f"Credits: {self.credits}, Tutor: {self.tutor}, Prüfungsform: {self.pruefungsform}")

