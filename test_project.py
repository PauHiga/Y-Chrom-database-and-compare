import pytest
from project import check_file_input, output_reading_error, combine_data, check_csv_data, prepare_user_input, check_user_input, compare_dicts, compare_dict_with_database, good_day

def test_check_file_input():
    assert check_file_input("path.docx", ".docx") == (False, "")
    assert check_file_input("", ".docx") == (True, "Error! \nNo .docx file was selected! \n:(\n\nPlease select a .docx file.")
    assert check_file_input("path.doc", ".docx") == (True, "Error! \nThe file selected is not a .docx file! \n:(\n\nPlease select a .docx file.")
    with pytest.raises(ValueError):
        check_file_input("", "")
    with pytest.raises(ValueError):
        check_file_input("path.doc.docx", "docx")

def test_output_reading_error():
    assert output_reading_error(["error1", "error2"]) == "The following sample/s could not be processed: \n\nerror1error2\nPlease check if the name of the samples is spelled exactly the same in each row of the original .docx table, -including whitespaces-, and check that the whole sample is in the same table (not several tables combined)" 
    assert output_reading_error([]) == ""

def test_combine_data():
    data1 = [{"M":"M1", "Y1":"1", "Y2":"2"}, {"M":"M2", "Y1":"1", "Y2":"2"}, {"M":"M4", "Y1":"1", "Y2":"2"}]
    data2 = [{"M":"M1", "Y1":"1", "Y2":"2"}, {"M":"M2", "Y1":"1", "Y2":"2"}, {"M":"M3", "Y1":"1", "Y2":"2"}]
    data3 = []
    data4 = []
    assert combine_data(data1, data2) ==  [{"M":"M3", "Y1":"1", "Y2":"2"}, {"M":"M1", "Y1":"1", "Y2":"2"}, {"M":"M2", "Y1":"1", "Y2":"2"}, {"M":"M4", "Y1":"1", "Y2":"2"}]
    assert combine_data(data1, data3) ==  [{"M":"M1", "Y1":"1", "Y2":"2"}, {"M":"M2", "Y1":"1", "Y2":"2"}, {"M":"M4", "Y1":"1", "Y2":"2"}]
    assert combine_data(data3, data4) ==  []

def test_check_csv_data():
    assert check_csv_data([]) == (True, "The selected database is empty! \nPlease pick a different file")
    assert check_csv_data(["Y1", "Y2", "Y3"]) == (True, "The selected file doesn't look like a .csv file created by this program. \nPlease select a database created by this program in order to compare your sample with it.")
    assert check_csv_data(["MUESTRA,DYS576,DYS389I,DYS448,DYS389II,DYS19,DYS391,DYS481,DYS549,DYS533,DYS438,DYS437,DYS570,DYS635,DYS390,DYS439,DYS392,DYS643,DYS393,DYS458,DYS385A/B,DYS456,Y-GATA-H4"]) == (False, "")

def test_prepare_user_input():
    user_input = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10', 10: '11', 11: '12', 12: '13', 13: '14', 14: '15', 15: '16', 16: '17', 17: '18', 18: '19', 19: '20', 20: '21', 21: '22'} 
    user_input2 = {0: 'nd', 1: 'ND', 2: 'Nd', 3: 'nD', 4: '  ND  ', 5: '  6  ', 6: '  7 ', 7: '8,8', 8: '9.9', 9: '10', 10: '11', 11: '12', 12: '13', 13: '14', 14: '15', 15: '16', 16: '17', 17: '18', 18: '19', 19: 'nd', 20: '21.2', 21: ''} 
    #Check all numbers input:
    assert prepare_user_input(user_input) == {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    #Check input with ND (upper and lower), whitespaces and points.
    assert prepare_user_input(user_input2) == {'DYS576': 'ND', 'DYS389I': 'ND', 'DYS448': 'ND', 'DYS389II': 'ND', 'DYS19': 'ND', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8,8', 'DYS533': '9,9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': 'ND', 'DYS456': '21,2', 'Y-GATA-H4': '', 'MUESTRA': 'Your sample'}

def test_check_user_input():
    # Check valid input (all numbers or ND, or xx/xx format for DYS385A/B
    user_input1 = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    assert check_user_input(user_input1) == (True, "")

    # Check invalid DYS385A/B (not match xx/xx format)
    user_input2 = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    assert check_user_input(user_input2) == (False, "DYS385A/B value should match xx/xx format. \nFor instance: 11/11")

    # Check missing DYS385A/B
    user_input3 = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    assert check_user_input(user_input3) == (False, "There is some error in the sample to compare, or some value is missing!\n\nThe values for the sample to compare can include numbers, the ND (Not determined) expression, or the xx/xx format for DYS385A/B")

    # Check missing value
    user_input4 = {'DYS576': '', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': 'ND', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    assert check_user_input(user_input4) == (False, "There is some error in the sample to compare, or some value is missing!\n\nThe values for the sample to compare can include numbers, the ND (Not determined) expression, or the xx/xx format for DYS385A/B")

def test_compare_dicts():
    # Checking no coincidences and ND count 
    dict_from_user = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    dict_from_user_with_ND = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': 'ND', 'DYS393': 'ND', 'DYS458': 'ND', 'DYS385A/B': 'ND', 'DYS456': 'ND', 'Y-GATA-H4': 'ND', 'MUESTRA': 'Your sample'}
    dict1 = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}
    dict2 = {'DYS576': '2', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}
    dict3 = {'DYS576': 'ND', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}
    dict4 = {'DYS576': 'ND', 'DYS389I': 'ND', 'DYS448': 'ND', 'DYS389II': 'ND', 'DYS19': 'ND', 'DYS391': 'ND', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}
    assert compare_dicts(dict_from_user, dict1) == "1º \"Your sample\" matches \"M001\"\n\n"
    assert compare_dicts(dict_from_user, dict2) == "2º \"Your sample\" matches \"M001\" with one exception\n\n"
    assert compare_dicts(dict_from_user, dict3) == "3º \"Your sample\" matches \"M001\" counting ND as potential match with 1 ND\n\n"
    assert compare_dicts(dict_from_user, dict4) == "4º \"Your sample\" matches \"M001\" counting ND as potential match, but keep in mind there are 6 ND in this comparison\n\n"
    assert compare_dicts(dict_from_user_with_ND, dict4) == "5º \"Your sample\" matches \"M001\" counting ND as potential match, but keep in mind there are 12 ND in this comparison\n\n"
    # Checking case of input from user vs mixed YDNA sample in database:
    dict_mixYDNA = {'DYS576': '1, 3', 'DYS389I': '2, 4', 'DYS448': '3, 6', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18, 14', 'DYS458': '19, 10', 'DYS385A/B': '20, 1, 19', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}
    assert compare_dicts(dict_from_user, dict_mixYDNA) == f"1º \"Your sample\" matches \"M001\"\n\n"

def test_compare_dict_with_database():
    dict_from_user = {'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'Your sample'}
    no_match = [{'DYS576': '0', 'DYS389I': '0', 'DYS448': '0', 'DYS389II': '0', 'DYS19': '0', 'DYS391': '0', 'DYS481': '0', 'DYS549': '0', 'DYS533': '0', 'DYS438': '0', 'DYS437': '0', 'DYS570': '0', 'DYS635': '0', 'DYS390': '0', 'DYS439': '0', 'DYS392': '0', 'DYS643': '0', 'DYS393': '0', 'DYS458': '0', 'DYS385A/B': '0', 'DYS456': '0', 'Y-GATA-H4': '0', 'MUESTRA': 'M001'}]
    list_of_dicts1 = [{'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}]
    list_of_dicts2 = [{'DYS576': '2', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}, {'DYS576': 'ND', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}, {'DYS576': 'ND', 'DYS389I': 'ND', 'DYS448': 'ND', 'DYS389II': 'ND', 'DYS19': 'ND', 'DYS391': 'ND', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}]
    list_of_dicts3 = [{'DYS576': '1', 'DYS389I': '2', 'DYS448': '3', 'DYS389II': '4', 'DYS19': '5', 'DYS391': '6', 'DYS481': '7', 'DYS549': '8', 'DYS533': '9', 'DYS438': '10', 'DYS437': '11', 'DYS570': '12', 'DYS635': '13', 'DYS390': '14', 'DYS439': '15', 'DYS392': '16', 'DYS643': '17', 'DYS393': '18', 'DYS458': '19', 'DYS385A/B': '20/20', 'DYS456': '21', 'Y-GATA-H4': '22', 'MUESTRA': 'M001'}, {'DYS576': '0', 'DYS389I': '0', 'DYS448': '0', 'DYS389II': '0', 'DYS19': '0', 'DYS391': '0', 'DYS481': '0', 'DYS549': '0', 'DYS533': '0', 'DYS438': '0', 'DYS437': '0', 'DYS570': '0', 'DYS635': '0', 'DYS390': '0', 'DYS439': '0', 'DYS392': '0', 'DYS643': '0', 'DYS393': '0', 'DYS458': '0', 'DYS385A/B': '0', 'DYS456': '0', 'Y-GATA-H4': '0', 'MUESTRA': 'M002'}, {'DYS576': '0', 'DYS389I': '0', 'DYS448': '0', 'DYS389II': '0', 'DYS19': '0', 'DYS391': '0', 'DYS481': '0', 'DYS549': '0', 'DYS533': '0', 'DYS438': '0', 'DYS437': '0', 'DYS570': '0', 'DYS635': '0', 'DYS390': '0', 'DYS439': '0', 'DYS392': '0', 'DYS643': '0', 'DYS393': '0', 'DYS458': '0', 'DYS385A/B': '0', 'DYS456': '0', 'Y-GATA-H4': '0', 'MUESTRA': 'M003'}]

    assert compare_dict_with_database(dict_from_user, no_match) == []
    assert compare_dict_with_database(dict_from_user, list_of_dicts1) == ["1º \"Your sample\" matches \"M001\"\n\n"]
    assert compare_dict_with_database(dict_from_user, list_of_dicts2) == ["2º \"Your sample\" matches \"M001\" with one exception\n\n", "3º \"Your sample\" matches \"M001\" counting ND as potential match with 1 ND\n\n", "4º \"Your sample\" matches \"M001\" counting ND as potential match, but keep in mind there are 6 ND in this comparison\n\n"]
    assert compare_dict_with_database(dict_from_user, list_of_dicts3) == ["1º \"Your sample\" matches \"M001\"\n\n"]

def test_good_day():
    assert good_day(3) == "Hello, good morning"
    assert good_day(11) == "Hello, good morning"
    assert good_day(12) == "Hello, good afternoon"
    assert good_day(17) == "Hello, good afternoon"
    assert good_day(18) == "Hello, good evening"
    assert good_day(2) == "Hello, good evening"
