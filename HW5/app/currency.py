import requests, psycopg2, os, sys, datetime
import xml.etree.ElementTree as ET

logs = []
query_params = "?date_req=02.03.2002"
date = datetime.datetime.strptime("02.03.2002", "%d.%m.%Y")
if len(sys.argv) > 1:
    date = datetime.datetime.strptime(sys.argv[1], "%d.%m.%Y")
    query_params = "?date_req=" + sys.argv[1]

response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp" + query_params)
logs.append("response status: " + str(response.status_code))

root = ET.fromstring(response.content)
logs.append(f"requested date {date.date()}")

currencyIDs = {"R01035", "R01235", "R01239"} # USD, EUR, GBP

conn_args = {
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
}
logs.append("connection arguments: " + str(conn_args))

with psycopg2.connect(**conn_args) as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS t_currency (
                id        BIGSERIAL   PRIMARY KEY,
                name      TEXT        NOT NULL DEFAULT '',
                char_code TEXT        NOT NULL DEFAULT '',
                value     DECIMAL     NOT NULL DEFAULT 0.0,
                date      TIMESTAMP   NOT NULL 
            );
            """
        )

        values = []
        isFirst = True
        for valute in root.findall("Valute"):
            valute_id = valute.get("ID")
            if valute_id in currencyIDs:
                if not isFirst:
                    values[-1] += ","
                isFirst = False
                
                char_code = valute.find("CharCode").text
                value = float(valute.find("Value").text.replace(",", ".", 1))
                name = valute.find("Name").text
                values.append(f"('{name}', '{char_code}', {value}, '{date}')")

                logs.append(f"currency with ID: {valute_id}, Value: {value}, Name: {name}, Date: {date}")

        insert_query = "INSERT INTO t_currency (name, char_code, value, date) VALUES\n" + "\n".join(values) + ";"
        logs.append("Insert query: " + insert_query)

        cursor.execute(insert_query)
        conn.commit()

with open("logs.txt", "a") as f:
    f.write("\n--------- start script ---------\n")
    f.write("\n".join(logs))
    f.write("\n---------- end script ----------\n")
