import pyodbc
from datetime import datetime

now = str(datetime.now()).split(" ")
date = now[0]

# DEBUGING
date = '2020-12-18'
# DEBUGING

conn = pyodbc.connect('Driver={SQL SERVER};'
                    'Server=(local);'
                    'Database=fss;'
                    'Trust_Connection=yes;')
cursor = conn.cursor()

statement_SO = f"SELECT * FROM fss.dbo.bsSaleOrder \
            WHERE DocDate >= '{date} 00:00:00' \
            AND DocDate <= '{date} 20:00:00'  \
            ORDER BY DocDate DESC"

def get_PO_list():
    statement_PO = f"SELECT * FROM fss.dbo.bsPR \
                WHERE DocDate >= '{date} 00:00:00' \
                AND DocDate <= '{date} 20:00:00'  \
                ORDER BY DocDate DESC"
    cursor.execute(statement_PO)

    result = []
    for row in cursor:
        result.append(row)
    
    return result


def get_PO_items(po_list):
    result_dict = {}
    item_list = []
    for p in po_list:
        PO_no = p[1]
        statement_PO_items = f"SELECT * FROM fss.dbo.bsPRItem \
                            WHERE DocNo = '{PO_no}'"
        cursor.execute(statement_PO_items)

        package = []
        for r in cursor:
            item_list.append(r)
            package.append(r)

        result_dict[r[1]] = package
    
    return result_dict, item_list


def counting_items(items_list):
    result = {}
    for item in items_list:
        item_name = item[4]
        amount = item[8]

        if item_name in result:
            result[item_name] += amount
        else:
            result[item_name] = amount

    return result


if __name__ == '__main__':
    # PO
    po_list = get_PO_list()
    po_items, raw_items_list = get_PO_items(po_list)

    print("="*30, "PO LIST", "="*30)
    for po in po_list:
        print('='*50)
        print(po[1])
        print('='*50)

        for item in po_items[po[1]]:
            print(item)
            print("*"*50)
    
    info_items = counting_items(raw_items_list)
    print(info_items)
