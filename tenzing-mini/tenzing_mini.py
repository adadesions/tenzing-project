import sys
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

statement_PO = f"SELECT * FROM fss.dbo.bsPR \
            WHERE DocDate >= '{date} 00:00:00' \
            AND DocDate <= '{date} 20:00:00'  \
            ORDER BY DocDate DESC"


def get_list(statement):
    cursor.execute(statement)
    result = []
    for row in cursor:
        result.append(row)
    
    return result


def get_items(list_, doc_type):
    data_table_names = {
        'PO': 'fss.dbo.bsPRItem',
        'SO': 'fss.dbo.bsSaleOrderItem'
    }
    result_dict = {}
    item_list = []
    try:
        table_name = data_table_names[doc_type]
    except KeyError as e:
        print(f"ERROR: DocType {e} not found")
        sys.exit()
        return {}, [] 

    for p in list_:
        doc_no = p[1]
        statement_items = f"SELECT * FROM {table_name}\
                            WHERE DocNo = '{doc_no}'"
        cursor.execute(statement_items)

        package = []
        for r in cursor:
            item_list.append(r)
            package.append(r)

        result_dict[r[1]] = package
    
    return result_dict, item_list


def counting_items(items_list, doc_type):
    qty_index = {
        'PO': 8, 'SO': 9
    }
    result = {}
    for item in items_list:
        item_name = item[4]
        amount = item[qty_index[doc_type]]

        if item_name in result:
            result[item_name] += amount
        else:
            result[item_name] = amount

    return result


def print_dict(dict_):
    for (k, v) in dict_.items():
        print(k, ":\t", v)

def print_doc_items(list_, list_items):
    print("="*30, "PO LIST", "="*30)
    for n in list_:
        print('='*50)
        print(n[1])
        print('='*50)

        for item in list_items[n[1]]:
            print(item)
            print("*"*50)

if __name__ == '__main__':
    # PO
    po_list = get_list(statement_PO)
    po_items, raw_items_list = get_items(po_list, 'PO')

    # SO
    so_list = get_list(statement_SO)
    so_items, raw_items_list = get_items(so_list, 'SO')

    print_doc_items(po_list, po_items)
    
    # info_items = counting_items(raw_items_list, 'PO')
    # print_dict(info_items)
