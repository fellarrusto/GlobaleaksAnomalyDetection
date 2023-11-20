import sys
import sqlite3
import csv
import json
from datetime import datetime
import numpy as np
import pandas as pd

def estimateAnomalyTreshold(cursor):
  # Recupera i dati dalla tabella
  cursor.execute('SELECT value FROM internaltipdata')
  result = cursor.fetchall()

  # Crea un DataFrame con i dati
  df = pd.DataFrame(result, columns=['value'])

  # Calcola la lunghezza delle stringhe
  df['length'] = df['value'].apply(len)

  bin_count = 10
  histogram_data, bin = np.histogram(df['length'], bins=bin_count)

  return bin[1]

def logData(entries, THR):
  # Stampa dei risultati
  for entry in entries:
      print("ID: %s, Creation Date: %s, Update Date: %s, Length of Value: %s, Identity Access Request Exists: %s, Identity Access Request Reply Authorized: %s, Status: %s, Possible anomaly: %s "
            % (
              str(entry[0]),
              str(datetime.strptime(entry[1], "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M")),
              str(datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M")),
              str(entry[3]),
              str(bool(entry[4])),
              str(bool(entry[5])),
              str(json.loads(entry[6]).get("it", json.loads(entry[6]).get("en"))),
              str("True" if entry[3]<THR else "False")
      )
  )

  with open('log_file.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      # Scrivi l'intestazione del CSV
      writer.writerow(["ID", "Creation Date", "Update Date", "Length of Value", "Identity Access Request Exists", "Identity Access Request Reply Authorized", "Status", "Possible Anomaly"])

      # Scrivi i dati
      for entry in entries:
          possible_anomaly = "True" if entry[3] < THR else "False"
          writer.writerow([
              entry[0],
              datetime.strptime(entry[1], "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M"),
              datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M"),
              entry[3],
              bool(entry[4]),
              bool(entry[5]),
              json.loads(entry[6]).get("it", json.loads(entry[6]).get("en")),
              possible_anomaly
          ])

def main(dbpath, csvpath):
  # Connessione al database SQLite
  conn = sqlite3.connect(dbpath)
  cursor = conn.cursor()

  # Stima soglia lunghezze anomale
  THR = estimateAnomalyTreshold(cursor)

  # Definizione query
  # Query SQL per estrarre i dati richiesti
  query = """
  SELECT 
      internaltipdata.internaltip_id,
      internaltip.creation_date,
      internaltip.update_date,
      LENGTH(internaltipdata.value),
      CASE 
          WHEN identityaccessrequest.id IS NOT NULL THEN 1 
          ELSE 0 
      END AS identityaccessrequest_exists,
      CASE 
          WHEN identityaccessrequest.reply = 'authorized' THEN 1 
          ELSE 0 
      END AS identityaccessrequest_reply,
      submissionstatus.label
  FROM 
      internaltipdata
  JOIN 
      internaltip ON internaltipdata.internaltip_id = internaltip.id
  LEFT JOIN 
      identityaccessrequest ON internaltip.id = identityaccessrequest.internaltip_id
  JOIN
      submissionstatus ON internaltip.status = submissionstatus.id
  """

  # Esecuzione della query
  cursor.execute(query)

  # Estrazione dei dati
  entries = cursor.fetchall()

  # Chiusura della connessione al database
  cursor.close()
  conn.close()

  logData(entries, THR)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: anomaly_detection.py <database>.db <logfile>.csv")
        sys.exit(1)

    database = sys.argv[1]
    logfile = sys.argv[2]

    main(database, logfile)
