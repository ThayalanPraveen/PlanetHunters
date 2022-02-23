import sys
import PySimpleGUI as sg
## file to test lightkurve functions

import numpy as np
import lightkurve as lk

## Search function
def search_star(target_name):
    if target_name == '':
        print("No Target Name input")
        return False
    else:
        search_result = lk.search_lightcurve(target_name)
        filtered = False
        return search_result , filtered , 0

## Reset function
def reset_search(target_name):
    search_result = lk.search_lightcurve(target_name)
    filtered = False
    return search_result, filtered , 0

## search filter function
def search_filter(identifier,value,target_name):
        search_result = lk.search_lightcurve(target_name)
        
        if identifier == '' or value == '':
            print("Please Select Identifier & Input valid Value")
            return 0,0,0
        else:
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                    value = str()
                    filter = np.where(search_result.table[identifier] == value)[0]
                    filtered = True
                    return search_result , filtered , filter
                else:
                    filter = np.where(search_result.table[identifier] == int(value))[0]
                    filtered = True
                    return search_result , filtered , filter
            except:
                filter = np.where(search_result.table[identifier] == int(value))[0]
                filtered = True
                return search_result , filtered , filter

## select star function
def select_star(hash_id,search_result,filtered,filter):
    if hash_id == '':
        print("Input valid #") ## finish validation
        return 0,0,0
    else:
        if filtered == True:
            lc = search_result[filter[int(hash_id)]].download()
        else:
            lc = search_result[int(hash_id)].download()
        return lc

## show search results function        
def show_search_results(search_results,filtered,filter):
    if filtered == False :
        return search_results
    else:
        return search_results[filter]

out = search_star("KIC 100000757") ## working search function
print(out)
search = select_star(0,out,filtered=False,filter= 0)
##out2 = show_search_results(search,False,0)
##print(out2[0])





username = ''
password = ''
#PROGRESS BAR
def progress_bar():
    sg.theme('LightBlue2')
    layout = [[sg.Text('Creating your account...')],
            [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
            [sg.Cancel()]]

    window = sg.Window('Working...', layout)
    for i in range(1000):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()


def create_account():
    global username, password
    sg.theme('DarkTeal10')
    layout = [[sg.Text("Sign Up", size =(15, 1), font=40, justification='c')],
             [sg.Text("E-mail", size =(15, 1),font=16), sg.InputText(key='-email-', font=16)],
             [sg.Text("Re-enter E-mail", size =(15, 1), font=16), sg.InputText(key='-remail-', font=16)],
             [sg.Text("Create Username", size =(15, 1), font=16), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=16), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Button("Submit"), sg.Button("Cancel")]]

    window = sg.Window("Sign Up", layout)

    while True:
        event,values = window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        else:
            if event == "Submit":
                password = values['-password-']
                username = values['-username-']
                if values['-email-'] != values['-remail-']:
                    sg.popup_error("Error", font=16)
                    continue
                elif values['-email-'] == values['-remail-']:
                    progress_bar()
                    break
    window.close()

def startapp():
    

def login():
    global username,password
    sg.theme('DarkTeal10')
    layout = [[sg.Text("Log In", size =(15, 1), font=40)],
            [sg.Text("Username", size =(15, 1), font=16),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Button('Ok'),sg.Button('Cancel'),sg.Button('Sign Up')]]

    window = sg.Window("Log In", layout)

    while True:
        event,values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif event == "Sign Up":
            create_account()
        else:
            if event == "Ok":
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    startapp()
                    break
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

    window.close()
login()