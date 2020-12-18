import pyodbc
from datetime import datetime

now = str(datetime.now()).split(" ")
date = now[0]
date = '2020-12-17'
conn = pyodbc.connect('Driver={SQL SERVER};'
                    'Server=(local);'
                    'Database=fss;'
                    'Trust_Connection=yes;')
cursor = conn.cursor()
statement_PO = f"SELECT * FROM fss.dbo.bsPR \
            WHERE DocDate >= '{date} 00:00:00' \
            AND DocDate <= '{date} 20:00:00'  \
            ORDER BY DocDate DESC"

statement_SO = f"SELECT * FROM fss.dbo.bsSaleOrder \
            WHERE DocDate >= '{date} 00:00:00' \
            AND DocDate <= '{date} 20:00:00'  \
            ORDER BY DocDate DESC"

cursor.execute(statement_SO)

counter = 0
for i, row in enumerate(cursor):
    print(row)
    print("="*50)
    counter += 1

print(f'Total rows = {counter}')
