#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#modulbuchung.py

# Importiere notwendige Module und Klassen
from datetime import datetime # Für korrekte Datumsanzeige
import pandas as pd # Importiere pandas für die Arbeit mit DataFrames

class Modulbuchung:
    """
    Repräsentiert eine Modulbuchung, die die Verbindung zwischen einem Studenten und einem Modul beschreibt.
    Beinhaltet Informationen über den Buchungsstatus, Prüfungsversuche und Ergebnisse.
    """
    def __init__(self, buchungsnummer, buchungsdatum, status, pruefungsversuch, pruefungsdatum=None, note=None, bestanden=False, modul_code=None, student_code=None, db_handler=None):
        """
        Initialisiert die Modulbuchung und lädt Modul- sowie Studentendaten.

        :param buchungsnummer: Eindeutige Nummer der Buchung.
        :param buchungsdatum: Datum der Buchung (als Timestamp oder None).
        :param status: Der Status der Buchung (z. B. "offen", "abgeschlossen").
        :param pruefungsversuch: Anzahl der Prüfungsversuche.
        :param pruefungsdatum: Datum der Prüfung (optional, als Timestamp oder None).
        :param note: Note der Prüfung (optional, als Float).
        :param bestanden: Status, ob die Prüfung bestanden wurde (als bool).
        :param modul_code: Code des zugehörigen Moduls.
        :param student_code: Code des zugehörigen Studenten.
        :param db_handler: Datenbankzugriffs-Handler für das Laden von Daten.
        """
        self.buchungsnummer = buchungsnummer
        self.buchungsdatum = buchungsdatum.to_pydatetime() if pd.notna(buchungsdatum) else None
        self.status = status
        self.pruefungsversuch = pruefungsversuch
        # Falls pruefungsdatum ein Timestamp ist, konvertiere ihn in einen String
        self.pruefungsdatum = datetime.strptime(pruefungsdatum.strftime('%Y-%m-%d'), '%Y-%m-%d') if pd.notna(pruefungsdatum) else None
        self.note = float(note) if note is not None else None
        self.bestanden = bool(bestanden)  # Sicherstellen, dass 'bestanden' als bool behandelt wird
        self.modul_code = modul_code
        self.student_code = student_code
        self.db_handler = db_handler

        # Modul- und Studenten-Objekte initialisieren
        self.modul = self.load_modul() if db_handler else None
        self.student = self.lade_student() if db_handler else None

    def load_modul(self):
        """
        Lädt die Daten des zugehörigen Moduls basierend auf modul_code aus der Datenbank.

        :return: Ein Modul-Objekt oder None, falls das Modul nicht gefunden wurde.
        """
        if not self.db_handler:
            raise ValueError("Kein DB-Handler vorhanden. Modul kann nicht geladen werden.")
        
        # Abrufen der Modul-Daten
        modul_data = self.db_handler.get_modul(self.modul_code)
        
        if modul_data is not None:
            # Debugging-Ausgabe der geladenen Daten
            print(f"Geladene Modul-Daten: {modul_data}")
            
            # Überprüfen, ob die erwarteten Spalten vorhanden sind
            if "modul_code" in modul_data.columns:
                return Modul(
                    modul_data["modul_code"].iloc[0], 
                    modul_data["modul_name"].iloc[0], 
                    modul_data["credits"].iloc[0], 
                    modul_data["tutor"].iloc[0], 
                    modul_data["pruefungsform"].iloc[0]
                )
            else:
                print(f"Spalte 'modul_code' nicht gefunden. Vorhandene Spalten: {modul_data.columns}")
        else:
            print(f"Kein Modul mit Code {self.modul_code} gefunden.")
        
        return None

    def lade_student(self):
        """
        Lädt die Daten des zugehörigen Studenten basierend auf student_code aus der Datenbank.

        :return: Ein Student-Objekt oder None, falls der Student nicht gefunden wurde.
        """
        if not self.db_handler:
            raise ValueError("Kein DB-Handler vorhanden. Student kann nicht geladen werden.")
        
        # Abrufen der Student-Daten
        student_data = self.db_handler.get_student(self.student_code)
        
        if student_data is not None:
            # Debugging-Ausgabe der geladenen Daten
            print(f"Geladene Student-Daten: {student_data}")
            
            # Überprüfen, ob die erwarteten Spalten vorhanden sind
            if "student_code" in student_data.columns:
                return Student(
                    student_data["student_code"].iloc[0], 
                    student_data["student_name"].iloc[0], 
                    student_data["start_studium"].iloc[0], 
                    student_data["zielnote"].iloc[0]
                )
            else:
                print(f"Spalte 'student_code' nicht gefunden. Vorhandene Spalten: {student_data.columns}")
        else:
            print(f"Kein Student mit Code {self.student_code} gefunden.")
        
        return None


    def show_status(self):
        """
        Gibt den Status der Modulbuchung zurück.

        :return: Ein Dictionary mit Statusinformationen.
        """
        return {
            "Buchungsnummer": self.buchungsnummer,
            "Status": self.status,
            "Prüfungsversuch": self.pruefungsversuch,
            "Bestanden": self.bestanden,
        }

    def ist_pruefung_bestanden(self):
        """
        Überprüft, ob die Prüfung bestanden wurde.

        :return: True, falls die Prüfung bestanden wurde, sonst False.
        """
        return self.bestanden

    def pruefungsinfo_anzeigen(self):
        """
        Gibt detaillierte Prüfungsinformationen zurück.

        :return: Ein Dictionary mit Prüfungsdetails.
        """
        return {
            "Buchungsnummer": self.buchungsnummer,
            "Prüfungsdatum": self.pruefungsdatum.strftime('%Y-%m-%d') if self.pruefungsdatum else "Kein Datum festgelegt",
            "Prüfungsversuch": self.pruefungsversuch,
            "Note": self.note,
            "Bestanden": self.bestanden,
        }

    def __str__(self):
        """
        Gibt eine String-Repräsentation der Modulbuchung zurück.

        :return: Eine formatierte Zeichenkette mit den Buchungsdetails.
        """
        modul_info = f"Modul: {self.modul.modul_name} (Code: {self.modul_code})" if self.modul else "Kein Modul"
        student_info = f"Student: {self.student.student_name} (Code: {self.student_code})" if self.student else "Kein Student"
        return f"Buchungsnummer: {self.buchungsnummer} | {modul_info} - {student_info} | Status: {self.status} | Prüfung: {self.pruefungsversuch} - Bestanden: {self.bestanden}"

class Modul:
    def __init__(self, modul_code, modul_name, credits, tutor, pruefungsform):
        self.modul_code = modul_code
        self.modul_name = modul_name
        self.credits = credits
        self.tutor = tutor
        self.pruefungsform = pruefungsform


class Student:
    def __init__(self, student_code, student_name, start_studium, zielnote):
        self.student_code = student_code
        self.student_name = student_name
        self.start_studium = start_studium
        self.zielnote = zielnote

