import xlwings
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
import itertools
# import gspread as gs

# data = load_workbook('data/sipkaren-tab.xlsx')
# data['group-a']['D2'].value = '0/6'
# data.save('data/sipkaren-tab.xlsx')

# excel_app = xlwings.App(visible=False)
# excel_book = excel_app.books.open('data/sipkaren-tab.xlsx')
# excel_book.save()
# excel_book.close()
# excel_app.quit()

# data = load_workbook('data/sipkaren-tab.xlsx', data_only=True)

def show_name_table():
    groups = ['group-a', 'group-b', 'group-b2','group-c']
    return groups



def show_table():
    valz = []
    groups = show_name_table()

    
    for g in groups:
        # gc = gs.service_account(filename='service_account.json')
        # sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1_thWOdagM4q6Cx2qdnToPNTuJrj8343b/edit')

        # ws = sh.worksheet(g)

        # df = pd.DataFrame(ws.get_all_records())
        data = pd.read_excel('website/static/data/sipkaren-tab.xlsx', g) 

        df = pd.DataFrame(data, columns=['Poradie', 'player','Body','Legy', 'plus'])
        # df = df.replace('?', np.NaN)
        df = df.sort_values(by=['Poradie'], ascending=True)

        
        # df = df.hide_index()
        # df = df.iloc[:,1:]
        # df.drop(columns = df.columns[0], axis = 0, inplace= True)
        der = df.to_string(index=False)
        der = df.values.tolist()
        
        # valz.append(der)
        # return der
        # valz = der
        # return valz
        # print(valz)
        # valz[g] = der[g]
        valz.append([der])
        # valz = append(der)
    return valz


def show_table_all():
    valz = []
    groups = show_name_table()

    
    for g in groups:
        # gc = gs.service_account(filename='service_account.json')
        # sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1_thWOdagM4q6Cx2qdnToPNTuJrj8343b/edit')

        # ws = sh.worksheet(g)

        # df = pd.DataFrame(ws.get_all_records())
        data = pd.read_excel('website/static/data/sipkaren-tab.xlsx', g) 

        df = pd.DataFrame(data, columns=['Poradie', 'player','Body','Legy', 'plus'])
        # df = df.replace('?', np.NaN)
        df = df.sort_values(by=['Poradie'], ascending=True)

        
        # df = df.hide_index()
        # df = df.iloc[:,1:]
        # df.drop(columns = df.columns[0], axis = 0, inplace= True)
        der = df.to_string(index=False)
        der = df.values.tolist()
        
        # valz.append(der)
        # return der
        # valz = der
        # return valz
        # print(valz)
        # valz[g] = der[g]
        valz.append(der)
        # valz = append(der)
    # return valz
    valz = itertools.chain(*valz)
    # res = str(list(valz))[1:-1]
    return list(valz)


# show_table_all()
