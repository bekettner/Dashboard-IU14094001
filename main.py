#!/usr/bin/env python
# coding: utf-8

# main.py

# Importiere notwendige Module und Klassen
from dbzugriff import DBZugriff  # Klasse zur Verwaltung der Datenbankzugriffe
from csvzugriff import CSVZugriff  # Klasse zum Arbeiten mit CSV-Dateien
from student import Student  # Klasse zur Repräsentation eines Studenten
import dashboard  # Modul zur Verwaltung des Dashboards

def main():
    """
    Hauptfunktion des Programms.
    - Initialisiert die Zugriffsobjekte (CSV und DB).
    - Holt die Studentendaten basierend auf Benutzereingabe.
    - Erstellt ein Student-Objekt und sammelt relevante Daten.
    - Startet das Dashboard mit den gesammelten Informationen.
    """
    # Erstelle eine Instanz von CSVZugriff
    csv_zugriff = CSVZugriff()  # Verwaltet den Zugriff auf die CSV-Datei

    # Erstelle eine Instanz von DBZugriff und übergebe die CSVZugriff-Instanz
    dbhandler = DBZugriff(csv_zugriff) # Schnittstelle zur Datenbank

    # Benutzereingabe für den Studenten-Code
    student_code = input("Bitte gib den Studenten-Code ein: ")

    # Versuche, die Studentendaten basierend auf dem Studenten-Code aus der Datenbank zu holen
    student_data = dbhandler.get_student(student_code)

    if student_data is not None and not student_data.empty:
        # Wenn die Daten existieren, extrahiere relevante Informationen
        print(f"Studenten-Daten für {student_code} gefunden. Starte Dashboard...")

        # Extrahiere spezifische Felder aus den Studentendaten
        student_name = student_data['student_name'].values[0]
        start_studium = student_data.iloc[0]["start_studium"]
        zielnote = student_data.iloc[0]["zielnote"]

        # Erstelle ein Student-Objekt mit den abgerufenen Informationen
        student = Student(
            student_code=student_code,
            student_name=student_name,
            start_studium=start_studium,
            zielnote=zielnote,
            db_handler=dbhandler
        )

        # Hole die verschiedenen Module des Studenten
        booked_not_completed_modules = dbhandler.get_booked_but_not_completed_modules(student_code)
        not_booked_modules = dbhandler.get_modules_not_booked_yet(student_code)
        completed_modules = dbhandler.get_completed_modules(student_code)
        
        # Erstelle eine grafische Darstellung der gesammelten Studienleistung
        student_plot = student.plot_combined_credits_per_semester()

        # Starte das Dashboard und übergebe alle gesammelten Daten
        dashboard.run_dashboard(student, booked_not_completed_modules, not_booked_modules, completed_modules)


    else:
        # Wenn keine Daten gefunden wurden, gib eine Fehlermeldung aus
        print(f"Kein Student mit dem Code {student_code} gefunden.")

# Prüft, ob die Datei direkt ausgeführt wird, und startet die Hauptfunktion
if __name__ == "__main__":
    main()


# 
