#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# student.py

# Importiere notwendige Module und Klassen
from datetime import datetime # Für korrekte Datumsanzeige
from dbzugriff import DBZugriff # Klasse zur Verwaltung der Datenbankzugriffe
from modulbuchung import Modulbuchung # Import von Modulbuchungen
import pandas as pd # Importiere pandas für die Arbeit mit DataFrames
import matplotlib.pyplot as plt # Für Diagramme
from studiengang import Studiengang  # Sicherstellen, dass Studiengang korrekt importiert wird

class Student:
    """
    Repräsentiert einen Studenten, einschließlich seiner Modulbuchungen und seines Studiengangs.
    """
    def __init__(self, student_code: str, student_name: str, start_studium: datetime, zielnote: float, db_handler):
        """
        Initialisiert ein Student-Objekt.

        :param student_code: Eindeutiger Code des Studenten.
        :param student_name: Name des Studenten.
        :param start_studium: Startdatum des Studiums.
        :param zielnote: Zielnote des Studenten.
        :param db_handler: Instanz des DBZugriff für Datenbankoperationen.
        """
        self.student_code = student_code
        self.student_name = student_name
        self.start_studium = start_studium
        self.zielnote = zielnote
        self.db_handler = db_handler
        self.studiengang = self.load_studiengang()  # Studiengang wird immer über den DB-Handler geladen
        self.modulbuchungen = self.load_modulbuchungen()  # Modulbuchungen werden immer über den DB-Handler geladen

    def load_studiengang(self):
        """
        Lädt den Studiengang des Studenten.

        :return: Instanz von Studiengang oder None, falls kein Studiengang gefunden wird.
        """
        student_studiengang_data = self.db_handler.get_student_studiengang(self.student_code)
        if student_studiengang_data is not None and not student_studiengang_data.empty:
            studiengang_code = student_studiengang_data.iloc[0]["studiengang_code"]
            studiengang_data = self.db_handler.read_data().get("studiengang.csv")
            studiengang_info = studiengang_data[studiengang_data["studiengang_code"] == studiengang_code].iloc[0]
            return Studiengang(
                studiengang_code=studiengang_info["studiengang_code"],
                studiengang_name=studiengang_info["studiengang_name"],
                erforderliche_credits=studiengang_info["benötigte_credits"],
                mindeststudienzeit=studiengang_info["anzahl_semester"]
            )
        else:
            print(f"Kein Studiengang für den Studenten {self.student_code} gefunden.")
            return None

    def load_modulbuchungen(self):
        """
        Lädt alle Modulbuchungen des Studenten.

        :return: Liste von Modulbuchung-Objekten.
        """
        modulbuchung_data = self.db_handler.get_modulbuchung(self.student_code)
        if modulbuchung_data is not None and not modulbuchung_data.empty:
            return [
                Modulbuchung(**row, db_handler=self.db_handler) for _, row in modulbuchung_data.iterrows()
            ]
        else:
            print(f"Keine Modulbuchungen für den Studenten {self.student_code} gefunden.")
            return []
            
    def calculate_total_credits(self) -> float:
        """
        Berechnet die insgesamt erreichten Credits des Studenten.

        :return: Summe der Credits aus bestandenen Modulbuchungen.
        """
        return sum(mb.modul.credits for mb in self.modulbuchungen if mb.bestanden)
    
    def calculate_average_grade(self) -> float:
        """
        Berechnet den Notendurchschnitt des Studenten.

        :return: Durchschnitt der Noten aus bestandenen Modulbuchungen oder None, falls keine vorhanden.
        """
        completed_modules = [mb for mb in self.modulbuchungen if mb.bestanden]
        if completed_modules:
            total_grades = sum(mb.note for mb in completed_modules)
            return total_grades / len(completed_modules)
        return None
    
    def calculate_missing_credits(self) -> float:
        """
        Berechnet die fehlenden Credits im Vergleich zu den erforderlichen Credits des Studiengangs.

        :return: Fehlende Credits.
        """
        required_credits = self.studiengang.erforderliche_credits if self.studiengang else 0
        achieved_credits = self.calculate_total_credits()
        return required_credits - achieved_credits

    def plot_combined_credits_per_semester(self):
        """
        Erstellt ein Balkendiagramm für:
        - Gesamte Credits pro Semester.
        - Credits aus bestandenen Modulen pro Semester.

        :return: Matplotlib-Figure oder None bei Fehlern.
        """
        try:
            # Prüfen, ob ein Studiengang vorhanden ist
            if self.studiengang is None:
                print(f"Kein Studiengang für den Studenten {self.student_code} gefunden.")
                return None
    
            studiengang_code = self.studiengang.studiengang_code
    
            # Daten für den Studiengang laden
            studiengang_semester_data = self.db_handler.get_studiengang_semester(studiengang_code)
            if studiengang_semester_data is None or studiengang_semester_data.empty:
                print(f"Keine Semester für den Studiengang {studiengang_code} gefunden.")
                return None
    
            semester_total_credits = {}
            semester_completed_credits = {}
    
            # Abgeschlossene Modulbuchungen des Studenten laden
            completed_modules = self.db_handler.get_completed_modules(self.student_code)
            if completed_modules is None or completed_modules.empty:
                print(f"Keine abgeschlossenen Module für den Studenten {self.student_code} gefunden.")
                return None
    
            # Für jedes Semester die Module laden und analysieren
            for _, semester_row in studiengang_semester_data.iterrows():
                semester_code = semester_row["semester_code"]
                semester_name = self.db_handler.get_semester(semester_code).iloc[0]["semester_name"] \
                    if not self.db_handler.get_semester(semester_code).empty else f"Semester {semester_code}"
                
                semester_module_data = self.db_handler.get_semester_modul(semester_code)
                if semester_module_data is None or semester_module_data.empty:
                    semester_total_credits[semester_name] = 0
                    semester_completed_credits[semester_name] = 0
                    continue
    
                total_credits = 0
                completed_credits = 0
    
                for _, module_row in semester_module_data.iterrows():
                    modul_code = module_row["modul_code"]
                    modul_data = self.db_handler.get_modul(modul_code)
                    if not modul_data.empty:
                        credits = modul_data.iloc[0]["credits"]
                        total_credits += credits
                        if modul_code in completed_modules["modul_code"].values:
                            completed_credits += credits
    
                semester_total_credits[semester_name] = total_credits
                semester_completed_credits[semester_name] = completed_credits
    
            # Daten für das Diagramm vorbereiten
            semesters = list(semester_total_credits.keys())
            total_credits_values = [semester_total_credits[sem] for sem in semesters]
            completed_credits_values = [semester_completed_credits[sem] for sem in semesters]
    
            # Diagramm erstellen
            x = range(len(semesters))
            width = 0.2  # Breite der Balken
    
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(x, total_credits_values, width=width, label="Gesamte Credits", color='skyblue', align='center')
            ax.bar([i + width for i in x], completed_credits_values, width=width, label="Bestandene Credits", color='green', align='center')
    
            # Diagramm beschriften
            ax.set_title(f"Credits pro Semester - Student: {self.student_name}")
            ax.set_xlabel("Semester")
            ax.set_ylabel("Credits")
            ax.set_xticks([i + width / 2 for i in x])
            ax.set_xticklabels(semesters, rotation=45)
            ax.legend()
            plt.tight_layout()
    
            return fig
    
        except Exception as e:
            print(f"Fehler beim Erstellen des Diagramms: {e}")
            return None

    def __str__(self) -> str:
        """
        Gibt eine String-Darstellung des Studenten zurück.

        :return: Formatierte Zeichenkette mit Studentendaten.
        """
        return (
            f"Student: {self.student_name} (Code: {self.student_code})\n"
            f"Startdatum: {self.start_studium.strftime('%d.%m.%Y')}\n"
            f"Zielnote: {self.zielnote:.2f}\n"
            f"Studiengang: {self.studiengang.studiengang_name if self.studiengang else 'Nicht gefunden'}\n"
            f"Anzahl Modulbuchungen: {len(self.modulbuchungen)}"
        )

