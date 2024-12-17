#!/usr/bin/env python
# coding: utf-8

# In[4]:


# csvzugriff.py

# Importiere notwendige Module und Klassen
import pandas as pd # Importiere pandas für die Arbeit mit DataFrames

class CSVZugriff:
    """
    Die Klasse CSVZugriff verwaltet den Zugriff auf eine Reihe von CSV-Dateien.
    Sie ermöglicht das Einlesen von Daten aus verschiedenen CSV-Dateien und die automatische
    Zuordnung von Datentypen sowie das Parsen von Datumsfeldern.
    """
    
    def __init__(self):
        """
        Initialisiert die Klasse und definiert die Pfade zu den CSV-Dateien,
        die zu verarbeitenden Spaltentypen und die Datumsspalten.
        """
        # Pfade zu den relevanten CSV-Dateien
        self.file_paths = [
            r"modul.csv",
            r"modulbuchung.csv",
            r"semester.csv",
            r"semester_modul.csv",
            r"student.csv",
            r"student_studiengang.csv",
            r"studiengang.csv",
            r"studiengang_semester.csv"
        ]
        
        # Definiert die Datentypen für spezifische Dateien und Spalten
        self.column_types = {
            "student.csv": {"student_code": str, "zielnote": float},
            "student_studiengang.csv": {"student_code": str, "studiengang_code": str},
            "modul.csv": {"modul_code": str, "credits": int},
            "modulbuchung.csv": {"student_code": str, "modul_code": str, "bestanden": bool},
            "semester.csv": {"semester_code": str},
            "semester_modul.csv": {"semester_code": str, "modul_code": str},
            "studiengang.csv": {"studiengang_code": str, "credits": int, "semester": int},
            "studiengang_semester.csv": {"studiengang_code": str, "semester_code": str}
        }

        # Definiere, welche Spalten als Datum geparst werden sollen
        self.date_columns = {
            "student.csv": ["start_studium"],  
            "modulbuchung.csv": ["buchungsdatum", "pruefungsdatum"],  
        }
        
    def read_data(self):
        """
        Liest alle CSV-Dateien in der Liste ein und gibt ein Dictionary zurück.
        Der Schlüssel ist der Dateiname, der Wert ist der eingelesene DataFrame.
        :return: Dictionary mit Dateinamen als Schlüssel und DataFrames als Werte
        """
        data_dict = {} # Dictionary zur Speicherung der geladenen DataFrames
        for file_path in self.file_paths:
            try:
                # Extrahiere den Dateinamen (z. B. "student.csv")
                file_name = file_path.split("\\")[-1]
                
                # Hole die definierten Datentypen und Datumsspalten für die aktuelle Datei
                dtype = self.column_types.get(file_name, None)
                parse_dates = self.date_columns.get(file_name, None)
                
                # Lade die CSV-Datei mit pandas, unter Berücksichtigung der Typ- und Datumseinstellungen
                data = pd.read_csv(file_path, dtype=dtype, parse_dates=parse_dates)
                
                # Speichere den DataFrame im Dictionary mit dem Dateinamen als Schlüssel
                data_dict[file_name] = data
                print(f"Datei {file_name} erfolgreich geladen.")  # Debugging: Bestätigung
            except FileNotFoundError:
                # Fehlerbehandlung, wenn die Datei nicht gefunden wird
                print(f"Datei nicht gefunden: {file_path}")
            except Exception as e:
                # Allgemeine Fehlerbehandlung mit Ausgabe der Fehlermeldung
                print(f"Fehler beim Lesen der Datei {file_path}: {e}")
        return data_dict

# Kurzer Test, um sicherzustellen, dass die CSV-Dateien geladen werden können
if __name__ == "__main__":
    """
    Führt einen Test des CSVZugriff-Moduls aus.
    Versucht, alle definierten CSV-Dateien zu laden, und gibt entsprechende Meldungen aus.
    """
    csv_zugriff = CSVZugriff()  # Instanziiere die CSVZugriff-Klasse
    csv_zugriff.read_data()  # Lese die CSV-Dateien ein und teste die Implementierung


# In[ ]:




