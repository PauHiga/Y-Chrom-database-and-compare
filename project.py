from docx import Document
import PySimpleGUI as sg
import csv
import os
import re
import datetime

def main():
    pysimplegui()

def pysimplegui():
    sg.theme('Dark Blue 3')
    database_created = ""

    layout = [[sg.HorizontalSeparator()],
        [ sg.Text('Welcome to "Y Chrom database and Compare"')],
        [sg.HorizontalSeparator()],  
        [sg.Text('This program creates a Y Chrom database extracting the data from .docx Word files.')], 
        [sg.Text('Then you can input a Y Chrom pattern to compare with the database.')], 
        [sg.Text('If you run this program for the first time, please start CREATING A DATABASE \nwith the button of the left')], 
        [sg.Text('')],
        [[sg.Button('Create or update Y Chrom Database', size = (20, 4))] + [sg.Button('Compare sample with a Y Chrom Database already created', size = (20, 4))]],
        [sg.Text('')], 
        [sg.HorizontalSeparator()], 
        [sg.Button('Exit', size = (10, 1))]]

    win1 = sg.Window('Y Chrom database and Compare', layout)
    win2_active=False
    win3_active=False
    while True:
        ev1, vals1 = win1.read()
        if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
            break

        if ev1 == 'Create or update Y Chrom Database'  and not win2_active:
            win2_active = True
            win1.Hide()
            layout_col1 = [[sg.Text('Create or update Y Chrom database')], 
                [sg.Text('This program creates a database extracting Y Chrom information from tables manually filled in .docx files.')], 
                [sg.Text('Please select a .docx file to extract the data from:')],
                [sg.InputText(key="docx-file-path"), sg.FileBrowse()],
                [sg.Text('If you pretend to UPDATE an already created database, please select the .csv file you wish to update:')],
                [sg.Text('If this field is empty, the program will use a default .csv file.')],
                [sg.InputText(key="save-in-file"), sg.FileBrowse()],
                [sg.Button('Create or Update Database', size = (15, 3))] + [sg.Text('', key='wait_for_process')],
                [sg.Text('')], 
                [sg.HorizontalSeparator()], 
                [sg.Button('Return', size = (10, 1))]]

            layout_col2 = [[sg.Multiline(good_day(), key='notes_create_db', size=(50,15))]]
            
            layout2 = [[sg.Col(layout_col1) , sg.VerticalSeparator(), sg.Col(layout_col2)]]

            win2 = sg.Window('Create or update Y Chrom database', layout2)
            while True:
                ev2, vals2 = win2.read()
                if ev2 == sg.WIN_CLOSED or ev2 == 'Return':
                    win2.close()
                    win2_active = False
                    win1.UnHide()
                    break
                if ev2 == 'Create or Update Database':
                    docx_path = vals2["docx-file-path"]
                    csv_path = vals2["save-in-file"]
                    # Check .docx input
                    if check_file_input(docx_path, ".docx")[0]:
                        sg.popup(check_file_input(docx_path, ".docx")[1])
                        win2['notes_create_db'].update(check_file_input(docx_path, ".docx")[1])
                    else:
                        # Add default .csv
                        if vals2["save-in-file"] == "":
                            csv_path = "default_Y Chrom_database.csv"
                        try: 
                            database_created = csv_path
                            write(combine_data(get_docx_data(docx_path)[0], get_csv_data(csv_path)), csv_path)
                            win2['notes_create_db'].update(f"database processed!\n:)\n\nYour database:\n{os.path.abspath(csv_path)}\n\n-----------------\n{output_reading_error(get_docx_data(docx_path)[1])}")
                            sg.popup(f"database processed!\n:)\n\nYour database:\n{os.path.abspath(csv_path)}")
                        except ValueError:
                            sg.popup("The selected file doesn't look like a .csv file created by this program, or some data is damaged. \nPlease select a .csv file created by this program to be updated.")
                            win2['notes_create_db'].update("The selected file doesn't look like a .csv file created by this program, or some data is damaged \nPlease select a .csv file created by this program to be updated.")


        if ev1 == 'Compare sample with a Y Chrom Database already created'  and not win3_active:
            win3_active = True
            win1.Hide()

            layout3_headings1 = ['DYS\n576','DYS\n389I','DYS\n448','DYS\n389II','DYS\n19','DYS\n391','DYS\n481','DYS\n549','DYS\n533','DYS\n438','DYS\n437']
            layout3_headings2 = ['DYS\n570', 'DYS\n635','DYS\n390','DYS\n439','DYS\n392','DYS\n643','DYS\n393','DYS\n458','DYS\n385A/B','DYS\n456','Y-GATA-\nH4']
            
            layout3_col1 = [[sg.Text('1- Select .csv database to compare with:')], 
                [sg.InputText(database_created, key='csv-to-compare'), sg.FileBrowse()],
                [sg.Text('')], 
                [sg.Text('2- Input the sample to compare with the selected database. Use either numbers or "ND" ("Not Determined").')], 
                [sg.Text(h, size=(5,2)) for h in layout3_headings1],
                [sg.Input(size=(7,1), pad=(0,0)) for cell in range(11)],
                [sg.Text(h, size=(5,2)) for h in layout3_headings2],
                [sg.Input(size=(7,1), pad=(0,0)) for cell in range(11)],
                [sg.Text('')], 
                [sg.Button('Compare!', size = (10, 2))], 
                [sg.Text('')], 
                [sg.Text('')], 
                [sg.HorizontalSeparator()], 
                [sg.Button('Return', size = (10, 1))]
                ]

            layout3_col2 = [[sg.Multiline(good_day(), key='Notes_compare', size=(50,15), disabled=True)]]
            
            layout3 = [[sg.Col(layout3_col1) , sg.VerticalSeparator(), sg.Col(layout3_col2)]]

            win3 = sg.Window('Compare Y Chrom pattern with database', layout3)
            while True:
                ev3, vals3 = win3.read()
                if ev3 == sg.WIN_CLOSED or ev3 == 'Return':
                    win3.close()
                    win3_active = False
                    win1.UnHide()
                    break
                csv_to_compare_data = vals3['csv-to-compare']
                # check .csv file to compare with:
                if ev3 == 'Compare!':
                    if check_csv_data(get_csv_data(csv_to_compare_data))[0]:
                        sg.popup(check_csv_data(get_csv_data(csv_to_compare_data))[1])
                        win3['Notes_compare'].update(check_csv_data(get_csv_data(csv_to_compare_data))[1])
                    else:
                        if check_user_input(prepare_user_input(vals3))[0]:
                            win3['Notes_compare'].update("".join(compare_databases(get_csv_data(csv_to_compare_data), [prepare_user_input(vals3)])))
                        else:
                            sg.popup(check_user_input(prepare_user_input(vals3))[1])
                            win3['Notes_compare'].update(check_user_input(prepare_user_input(vals3))[1])
    win1.close()


def check_file_input(path: str, ext: str):
    filename, file_extension = os.path.splitext(path)
    if not re.search(r"^\.\w+$", ext):
        raise ValueError('"ext" argument is not valid') 
    if filename == '':
        return True, f'Error! \nNo {ext} file was selected! \n:(\n\nPlease select a {ext} file.'
    elif file_extension != ext:
        return True, f'Error! \nThe file selected is not a {ext} file! \n:(\n\nPlease select a {ext} file.'
    else:
        return False, ''

def get_docx_data(document):
    document = Document(document)
    tables = document.tables
    docx_data = []
    check_this_tables = []

    for table in tables:
        table_headers = []
        table_samples_values = []

        raw_docxrows = [[cell.text.strip().replace("\n", "").replace(".", ",").upper() for cell in row.cells] for row in table.rows]

        first_column_values = set(cell.text.strip().replace("\n", "").upper() for cell in table.columns[0].cells)   

        first_marker_in_header = table.rows[0].cells[1].text.strip().replace("\n", "").upper()

        column_values_list = list(first_column_values)
        
        for i in range(len(column_values_list)):
            full_row = []
            for item in raw_docxrows:
                if column_values_list[i] in item:
                    item.remove(column_values_list[i])
                    full_row.extend(list(filter(None, item)))

            full_row_complete = [column_values_list[i]]
            full_row_complete.extend(full_row)

            if first_marker_in_header in full_row_complete:
                table_headers = tuple(full_row_complete)
            else:    
                table_samples_values.append(tuple(full_row_complete))

        for sample_values in table_samples_values:
            if len(sample_values) != 23:
                check_this_tables.append(f"{sample_values[0]}\n")
            else:
                data = {table_headers[i]:sample_values[i] for i in range(len(table_headers))}
                docx_data.append(data)
    return docx_data, check_this_tables

def output_reading_error(check_this_tables: list):
    if check_this_tables != []:
        error_in_tables = "".join(check_this_tables)
        return f"The following sample/s could not be processed: \n\n{error_in_tables}\nPlease check if the name of the samples is spelled exactly the same in each row of the original .docx table, -including whitespaces-, and check that the whole sample is in the same table (not several tables combined)" 
    else:
        return ""

def get_csv_data(csvfile: str): 
    csvdata = []
    try:
        with open(csvfile) as file:
            reader = csv.DictReader(file)
            for row in reader:
                csvdata.append(row)
    except FileNotFoundError:
        pass
    return csvdata

def combine_data(doc_data, csv_data):
    finaldata = csv_data.copy()
    finaldata.extend(doc_data)
    no_repeat_data = [finaldata[i] for i in range(len(finaldata)) if finaldata[i] not in finaldata[i + 1:]]
    return no_repeat_data

def write(data, exitfile):
    fieldnames_data = [item for item in data[0]]    
    with open(exitfile, "w", newline='') as file:       
        writer = csv.DictWriter(file, fieldnames=fieldnames_data)
        writer.writeheader()
        for item in data:    
            writer.writerow(item)

def check_csv_data(csv_data):
    if csv_data == []: 
        return True, "The selected database is empty! \nPlease pick a different file"
    elif "Y-GATA-H4" not in csv_data[0] or "DYS389I" not in csv_data[0]:
        return True, "The selected file doesn't look like a .csv file created by this program. \nPlease select a database created by this program in order to compare your sample with it."
    else:
        return False, ""

def prepare_user_input(user_input):
    headers = ['MUESTRA','DYS576','DYS389I','DYS448','DYS389II','DYS19','DYS391','DYS481','DYS549','DYS533','DYS438','DYS437','DYS570','DYS635','DYS390','DYS439','DYS392','DYS643','DYS393','DYS458','DYS385A/B','DYS456','Y-GATA-H4']
    for i in range(len(headers)-1):
        sample = {headers[i+1]: user_input[i].strip().upper().replace(".", ",") for i in range(len(headers)-1)}
    sample['MUESTRA']= 'Your sample'
    return sample

def check_user_input(user_input):
    keys = ['MUESTRA','DYS576','DYS389I','DYS448','DYS389II','DYS19','DYS391','DYS481','DYS549','DYS533','DYS438','DYS437','DYS570','DYS635','DYS390','DYS439','DYS392','DYS643','DYS393','DYS458','DYS385A/B','DYS456','Y-GATA-H4']
    accepted_input = 0
    for key in keys:
        if key == "DYS385A/B": 
            if user_input[key] == "":
                return False, "There is some error in the sample to compare, or some value is missing!\n\nThe values for the sample to compare can include numbers, the ND (Not determined) expression, or the xx/xx format for DYS385A/B"
            if re.search(r"^(\d*/\d*)|(ND)$", user_input[key]):
                accepted_input += 1
            else:
                return False, "DYS385A/B value should match xx/xx format. \nFor instance: 11/11"
        elif re.search(r"[0-9,]|ND$", user_input[key]):
            accepted_input += 1
    if accepted_input != 22:
        return False, "There is some error in the sample to compare, or some value is missing!\n\nThe values for the sample to compare can include numbers, the ND (Not determined) expression, or the xx/xx format for DYS385A/B"
    elif accepted_input == 22:
        return True, ""

def compare_databases(list_of_dict_database, list_of_dict_to_compare):
    matches = [compare_dict_with_database(each_dict_to_compare, list_of_dict_database) for each_dict_to_compare in list_of_dict_to_compare if compare_dict_with_database(each_dict_to_compare, list_of_dict_database) != None]
    all_matches = []
    for item in matches:
        all_matches.extend(item)
    return all_matches

def compare_dict_with_database(each_comparison, database):
    current_sample_match = []
    for database_dict in database:
        if compare_dicts(each_comparison, database_dict) != None:
            current_sample_match.append(compare_dicts(each_comparison, database_dict))
    return sorted(current_sample_match)

def compare_dicts(dict_sample, dict_database):
    return_message = ""
    full_dict_matches = []
    dict_matches_with_ND = []
    for key in list(dict_sample)[0:]:
        if key == 'MUESTRA':
            pass
        if key == 'DYS385A/B':
            if dict_sample[key] == "ND":
                dict_matches_with_ND.append(dict_sample[key])
            else:
                first, last = dict_sample[key].split('/')
                if dict_database[key] == 'ND' or dict_database[key] == '*':
                    dict_matches_with_ND.append(dict_sample[key])

                elif first in dict_database[key] and last in dict_database[key]:
                    dict_matches_with_ND.append(dict_sample[key])
                    full_dict_matches.append(dict_sample[key])
        else:
            if dict_sample[key] in dict_database[key] and dict_sample[key] != 'ND':
                full_dict_matches.append(dict_sample[key])
                dict_matches_with_ND.append(dict_sample[key]) 
                
            elif dict_sample[key] in dict_database[key] or (dict_sample[key] == 'ND' or dict_database[key] == 'ND' or dict_database[key] == '*'):
                dict_matches_with_ND.append(dict_sample[key])     

    ND_alone = len(dict_matches_with_ND) - len(full_dict_matches)

    if len(full_dict_matches) == 22:
        return_message = f"1º \"{dict_sample['MUESTRA']}\" matches \"{dict_database['MUESTRA']}\"\n\n"
    elif len(full_dict_matches) == 21 and len(dict_matches_with_ND) != 22:
        return_message = f"2º \"{dict_sample['MUESTRA']}\" matches \"{dict_database['MUESTRA']}\" with one exception\n\n"
    
    elif len(dict_matches_with_ND) == 22 and len(full_dict_matches) >= 17:
        return_message = f"3º \"{dict_sample['MUESTRA']}\" matches \"{dict_database['MUESTRA']}\" counting ND as potential match with  {ND_alone} ND\n\n"
    elif len(dict_matches_with_ND) == 22 and len(full_dict_matches) >= 10:
        return_message = f"4º \"{dict_sample['MUESTRA']}\" matches \"{dict_database['MUESTRA']}\" counting ND as potential match, but keep in mind there are {ND_alone} ND in this comparison\n\n"
    elif len(dict_matches_with_ND) == 22:
        return_message = f"5º \"{dict_sample['MUESTRA']}\" matches \"{dict_database['MUESTRA']}\" counting ND as potential match, but keep in mind there are {ND_alone} ND in this comparison\n\n"

    return return_message


def good_day():
    if 4 < datetime.datetime.now().hour <= 11:
        return "Hello, good morning"
    elif 11 < datetime.datetime.now().hour <= 17:
        return "Hello, good afternoon"
    elif 17 < datetime.datetime.now().hour <= 21:
        return "Hello, good evening"
    else:
        return "Hello, good night"

if __name__ == "__main__":
    main()

