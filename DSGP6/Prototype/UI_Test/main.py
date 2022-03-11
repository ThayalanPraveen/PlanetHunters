from glob import glob
import json
import tkinter
import os
import lightkurve as lk
import matplotlib.pyplot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import PySimpleGUI as sg
from pandas import array
import requests
import firebase_admin
from firebase_admin import db

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Prototype/UI_Test/planet-hunters-1b294-firebase-adminsdk-ksboi-00cff64782.json")
firebase_admin.initialize_app(cred , {
    'databaseURL': 'https://planet-hunters-1b294-default-rtdb.firebaseio.com'
})


apikey='AIzaSyAqvXwzaDvA3F3xkhHzbAGWmswYu5NDAds'# the web api key

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
                        params={"key": apikey},
                        data=payload)

    if 'error' in r.json().keys():
        return {'status':'error','message':r.json()['error']['message']}
    #if the login succeeded
    if 'idToken' in r.json().keys() :
            return {'status':'success','idToken':r.json()['idToken']}

    return r.json()

def NewUser(email,password):
    details={
        'email':email,
        'password':password,
        'returnSecureToken': True
    }
    # send post request
    r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey),data=details)
    #check for errors in result
    if 'error' in r.json().keys():
        return {'status':'error','message':r.json()['error']['message']}
    #if the registration succeeded
    if 'idToken' in r.json().keys() :
            return {'status':'success','idToken':r.json()['idToken']}

progress = False
name = ''
f = False
T_name = ""
author = ""
Filter = None
lc = None
fig = ''
exo = 0
search_result = []
exit = False
S_Font = ('Helvetica', 20)
S_Font2 = ('Helvetica', 18)
S_Font3 = ('Helvetica', 15)
sg.theme('DarkTeal10')
username = ''

while True:
    
    def habitabilityScreen():
        return

    def startScreen():
        global exit
        layout = [[sg.Button('Exoplanet Detection', font=S_Font2),
                   sg.Button('Habitability Detection', font=S_Font2)]]

        window = sg.Window('Planet Hunters', layout, size=(395, 100))
        while True:
            event, values = window.read()
            if event == 'Exoplanet Detection':
                window.close()
                searchScreen()
                break
            elif event == 'Habitability Detection':
                window.close()
                habitabilityScreen()
                break
            if event == 'WIN_CLOSED':
                exit = True
                window.close()
            if event in (None, 'Exit'):
                exit = True
                window.close()

    def progress_bar():
        global T_name
        global author
        global search_result
        layout = [[sg.Text('Collecting data from database...')],
                [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progbar')],
                [sg.Cancel()]]
        window = sg.Window('Working...', layout)
        search_result = lk.search_lightcurve(T_name)
        for i in range(100):
            event, values = window.read(timeout=1)
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            window['progbar'].update_bar(i + 10)
        window.close()

    def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
        if canvas.children:
            for child in canvas.winfo_children():
                child.destroy()
        if canvas_toolbar.children:
            for child in canvas_toolbar.winfo_children():
                child.destroy()
        figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
        toolbar.update()
        figure_canvas_agg.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    class Toolbar(NavigationToolbar2Tk):
        def __init__(self, *args, **kwargs):
            super(Toolbar, self).__init__(*args, **kwargs)

    def progress_bar2():
        layout = [[sg.Text('Creating your account...')],
                [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progbar')],
                [sg.Cancel()]]
        window = sg.Window('Working...', layout)
        for i in range(100):
            event, values = window.read(timeout=1)
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            window['progbar'].update_bar(i + 10)
        window.close()


    def create_account():
        global exit
        layout = [[sg.Text("Sign Up", size =(15, 1), font=40, justification='c')],
                [sg.Text("E-mail", size =(15, 1),font=16), sg.InputText(key='-email-', font=16)],
                [sg.Text("Re-enter E-mail", size =(15, 1), font=16), sg.InputText(key='-remail-', font=16)],
                [sg.Text("Create Password", size =(15, 1), font=16), sg.InputText(key='-password-', font=16, password_char='*')],
                [sg.Button("Submit"), sg.Button("Cancel"),sg.Button("Login")]]

        window = sg.Window("Sign Up", layout)

        while True:
            event,values = window.read()
            if event == 'WIN_CLOSED':
                exit = True
                window.close()
                break
            elif event in (None, 'Exit'):
                exit = True
                window.close()
                break
            else:
                if event == "Login" :
                    window.close()
                    login()
                    break
                if event == "Submit":
                    password = values['-password-']
                    if values['-email-'] != values['-remail-']:
                        sg.popup_error("Error", font=16)
                        continue
                    elif values['-email-'] == values['-remail-']:
                        progress_bar2()
                        test = NewUser(values['-email-'],password)
                        if test['status'] == 'success' :
                            sg.popup("Thank you for signing up, please login now", font=16)
                            test = values['-email-']
                            test = test.replace("@","")
                            test = test.replace(".","")
                            ref = db.reference('/users')
                            ref.set({
                                test : {
                                    'History': { "array" : [0] }
                                }
                            })
                            window.close()
                            login()
                            break
                        else:
                            sg.popup_error("Error %f",test['message'], font=16)
                            window.close()
                            create_account()
                        break
        window.close()


    def login():
        global exit
        global username
        layout = [[sg.Text("Log In", size =(15, 1), font=40)],
                [sg.Text("Email", size =(15, 1), font=16),sg.InputText(key='-email-', font=16)],
                [sg.Text("Password", size =(15, 1), font=16),sg.InputText(key='-pwd-', password_char='*', font=16)],
                [sg.Button('Ok'),sg.Button('Cancel'),sg.Button('Sign Up')]]

        window = sg.Window("Log In", layout)

        while True:
            event,values = window.read()
            if event == 'WIN_CLOSED':
                exit = True
                window.close()
                break
            elif event in (None, 'Exit'):
                exit = True
                window.close()
                break
            elif event == "Sign Up":
                window.close()
                create_account()
                break
            else:
                if event == "Ok":
                    token = sign_in_with_email_and_password(values['-email-'], values['-pwd-'])
                    if token['status'] == 'success' :
                        test = values['-email-']
                        test = test.replace("@","")
                        test = test.replace(".","")
                        username = test
                        sg.popup("Welcome!", font=16)
                        window.close()
                        startScreen()
                        break
                    else:
                        sg.popup_error("Error %f",token['message'], font=16)
                        window.close()
                        login()
                    break
        window.close()

    def searchScreen():
        global username
        global progress
        global f
        global T_name
        global author
        global exo
        global filter
        global lc
        global fig
        global search_result
        global exit
        progress = False
        f = False
        layout = [[sg.Text('Search Exoplanet with Target name & Author', font=S_Font)],
                  [sg.Text('Target Name:', font=S_Font2),
                   sg.InputText('TIC 145241359', font=S_Font2)],
                  [sg.Button('Search', font=S_Font2),
                   sg.Button('Exit', font=S_Font2),sg.Button('Suggested Targets', font=S_Font2),sg.Button('History', font=S_Font2)],]

        window = sg.Window('Exoplanet Analyzer', layout, size=(700, 150))
        while True:
            event, values = window.read()
            if event == "Suggested Targets" :
                pass
            if event == "History" :
                window.close()
                history()
                break

            if event == 'Search':
                T_name = values[0]
                if T_name == '' :
                    sg.Popup("No Target Name ", font=S_Font2)
                    window.close()
                    searchScreen()
                    break
                else:
                    if progress == False:
                        progress_bar()
                        progress = True
                    hist_array = []
                    ref = db.reference('/users')
                    users_ref = ref.child(username)
                    user_data = users_ref.get()
                    hist_array = user_data['History']['array']
                    if hist_array[0] == 0 :
                        hist_array[0] = T_name
                    else:
                        hist_array.append(T_name)
                    
                    users_ref.update({

                        'History': {"array" : hist_array }
                    })
                    window.close()
                    selectScreen()
                    break
            if event == 'WIN_CLOSED':
                exit = True
                window.close()
                break
            if event in (None, 'Exit'):
                exit = True
                window.close()
                break

    def filterScreen():
        global f
        global T_name
        global author
        global exo
        global filter
        global lc
        global fig
        global search_result
        global exit
        layout2 = [[sg.Text('Search using specific identifier', font=S_Font2)],
                   [sg.Text('Identifier: ', font=S_Font2),
                    sg.Listbox(
                        values=['dataproduct_type', 'calib_level', 'obs_collection', 'obs_id', 'target_name', 's_ra',
                                's_dec', 't_min', 't_max', 't_exptime', 'wavelength_region', 'filters', 'em_min',
                                'em_max', 'target_classification', 'obs_title', 't_obs_release', 'instrument_name',
                                'proposal_pi', 'proposal_id', 'proposal_type', 'project', 'sequence_number',
                                'provenance_name', 's_region', 'jpegURL', 'dataURL', 'dataRights', 'mtFlag', 'srcDen',
                                'intentType', 'obsid', 'objID', 'exptime', 'distance', 'obsID',
                                'obs_collection_products', 'dataproduct_type_products', 'description', 'type',
                                'dataURI', 'productType', 'productGroupDescription', 'productSubGroupDescription',
                                'productDocumentationURL', 'project_products', 'prvversion', 'proposal_id_products',
                                'productFilename', 'size', 'parent_obsid', 'dataRights_products',
                                'calib_level_products', 'author', 'mission', '#', 'year', 'sort_order'],
                        select_mode='single', key='fac', font=S_Font2, size=(30, 10))],
                   [sg.Text('Value: ', font=S_Font2),
                    sg.InputText('', font=S_Font2)],
                   [sg.Submit('Search', font=S_Font2),
                    sg.Button('Back', font=S_Font2),
                    sg.Button('Exit', font=S_Font2)]]
        window2 = sg.Window('Advanced Search', layout2, size=(480, 700))
        while True:
            event, values = window2.read()
            if event == 'Back':
                window2.close()
                selectScreen()
                break
            if event == 'WIN_CLOSED':
                exit = True
                window2.close()
                break
            if event in (None, 'Exit'):
                exit = True
                window2.close()
                break
            if event == 'Search':
                search_result = lk.search_lightcurve(T_name, author=author)
                print("T_name is :",T_name)
                print("author is :",author)
                print("search is :",search_result)
                f_by = values['fac']
                f_val = values[0]
                if f_by == '' or f_val == '':
                    sg.Popup("Please Select Identifier & Input valid Value", font=S_Font2)
                    window2.close()
                    filterScreen()
                    break
                else:
                    if f_val.startswith('"') and f_val.endswith('"'):
                        f_val = f_val[1:-1]
                        f_val = str(f_val)
                        Filter = np.where(search_result.table[f_by[0]] == f_val)[0]
                    else:
                        Filter = np.where(search_result.table[f_by[0]] == int(f_val))[0]
                    f = True
                    window2.close()
                    selectScreen()
                    break

    def history():
        global username
        global T_name
        hist_array = []
        ref = db.reference('/users')
        users_ref = ref.child(username)
        user_data = users_ref.get()
        hist_array = user_data['History']['array']
        string = ""
        for x in range(0,len(hist_array)):
            string = string + hist_array[x] + "\n"

        layout = [[sg.Listbox(values = hist_array, size=(31,6), font=S_Font2 , key='hist')],
                  [sg.Button('Search', font=S_Font2),sg.Button('Clear History', font=S_Font2),sg.Button('Back to Search', font=S_Font2)]]

        window = sg.Window('History', layout, size=(395, 200))
        while True:
            event, values = window.read()
            if event == 'Search' :
                T_name = values['hist'][0]
                print(T_name)
                progress_bar()
                window.close()
                selectScreen()
                break
            if event == 'Back to Search' :
                window.close()
                searchScreen()
                break
            if event == 'WIN_CLOSED':
                exit = True
                window.close()
                break
            if event in (None, 'Exit'):
                exit = True
                window.close()
                break


    def selectScreen():
        global f
        global T_name
        global author
        global exo
        global filter
        global lc
        global fig
        global search_result
        global exit
        global progress
        if f == True:
            layout3 = [
                [sg.Text(search_result[Filter], font=S_Font3, justification='left')],
                [sg.Text('#', font=S_Font2), sg.InputText('', font=S_Font2)],
                [sg.Button('Select Data', font=S_Font2),
                 sg.Button('Advanced Filter', font=S_Font2),
                 sg.Button('Reset', font=S_Font2)],
                [sg.Button('Back To Search', font=S_Font2), sg.Button('Exit', font=S_Font2)]]
        else:
            layout3 = [
                [sg.Text(search_result, font=S_Font3, justification='left')],
                [sg.Text('#', font=S_Font2), sg.InputText('', font=S_Font2)],
                [sg.Button('Select Data', font=S_Font2),
                 sg.Button('Advanced Filter', font=S_Font2),
                 sg.Button('Reset', font=S_Font2)],
                [sg.Button('Back To Search', font=S_Font2), sg.Button('Exit', font=S_Font2)]]

        window3 = sg.Window('Results', layout3, size=(480, 700), resizable=True)
        event, values = window3.read()
        if event == 'Reset':
            f = False
            window3.close()
            selectScreen()
        if event == 'Back To Search':
            window3.close()
            searchScreen()
        if event == 'WIN_CLOSED':
            window3.close()
            exit = True
        if event in (None, 'Exit'):
            window3.close()
            exit = True
        if event == 'Advanced Filter':
            window3.close()
            filterScreen()
        if event == 'Select Data':
            if values[0] == '':
                sg.Popup("Input valid #", font=S_Font2)
                window3.close()
                selectScreen()
            else:
                exo = values[0]
                if f == True:
                    lc = search_result[Filter[int(exo)]].download()
                else:
                    lc = search_result[int(exo)].download()
                window3.close()
                plotsScreen()

    def plotsScreen():
        global f
        global T_name
        global author
        global exo
        global filter
        global lc
        global fig
        global search_result
        global exit
        layout5 = [
            [sg.T('Graph: Light Curve')],
            [sg.B('Light Curve'), sg.B('Flattened LC'), sg.B('Folded')],
            [sg.T('Controls:')],
            [sg.Canvas(key='controls_cv')],
            [sg.T('Figure:')],
            [sg.Column(
                layout=[
                    [sg.Canvas(key='fig_cv',
                               # it's important that you set this size
                               size=(400 * 2, 400,)
                               )]
                ],
                background_color='#DAE0E6',
                pad=(0, 0)
            )],
            [sg.B('Back')]
        ]
        window5 = sg.Window('Graph with controls', layout5)
        while True:
            event, values = window5.read()
            if event in (sg.WIN_CLOSED, 'Back'):  # always,  always give a way out!
                window5.close()
                selectScreen()
                break

            if event == 'Flattened LC':
                plt.close("all")
                flat_lc = lc.flatten()
                flat_lc.plot()
                fig = matplotlib.pyplot.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(400 * 2 / float(DPI), 400 / float(DPI))
                draw_figure_w_toolbar(window5['fig_cv'].TKCanvas, fig, window5['controls_cv'].TKCanvas)

            if event == 'Light Curve':
                lc.plot()
                fig = matplotlib.pyplot.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(400 * 2 / float(DPI), 400 / float(DPI))
                draw_figure_w_toolbar(window5['fig_cv'].TKCanvas, fig, window5['controls_cv'].TKCanvas)

            if event == 'Folded':
                flat_lc = lc.flatten()
                periodogram = flat_lc.to_periodogram(method="bls")
                best_fit_period = periodogram.period_at_max_power
                folded_lc = flat_lc.fold(period=best_fit_period)
                folded_lc.plot()
                fig = matplotlib.pyplot.gcf()
                DPI = fig.get_dpi()
                fig.set_size_inches(400 * 2 / float(DPI), 400 / float(DPI))
                draw_figure_w_toolbar(window5['fig_cv'].TKCanvas, fig, window5['controls_cv'].TKCanvas)
    if exit == False:
        login()
    else:
        break