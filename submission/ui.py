import os
import PySimpleGUI as sg
import sys

from handler import Handler

 


main_window = None
def save_file_window():
    layout = [[sg.Text("Save a new file")],
              [sg.Text("Select file to upload"), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
              [sg.Text("Enter password"), sg.Input(key="-PASSWORD-", password_char="*")],
              [sg.Text("Select public Key file"), sg.Input(key="-PUBLICKEYFILE-"), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
              [sg.Text("Enter Video Title"), sg.Input(key="-TiTLE-")],
              [sg.Text("Enter Video Description"), sg.Input(key="-DESCRIPTION-")],
              [sg.Button("Submit"), sg.Button("Cancel")]]

    window = sg.Window("Save a file", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return "no file was chosen", "null"
        elif event == "Submit":
            file_path = values["-FILE-"]
            public_key_file_path = values["-PUBLICKEYFILE-"]
            password = values["-PASSWORD-"]
            title = values["-TiTLE-"]
            description = values["-DESCRIPTION-"]
            print(f"File path: {file_path}")
            print(f"Password: {password}")
            main_window["-TERMINAL-"].update(f"File path: {file_path}\ncreating video please wait...")
            window.close()
            handler = Handler(MainWindow=main_window)
            ret = handler.save(file_path, password,public_key_file_path ,title, description)
            main_window["-TERMINAL-"].update(f"File path: {file_path}\ncreating video please wait...\n{ret}")
            return file_path, password

    
def retrieve_file_window():
    layout = [[sg.Text("Retrieve an already saved file")],
              [sg.Text("Select Youtube video to upload"), sg.Input(key="-YOUTUBE_LINK-"), sg.FileBrowse(file_types=(("All Files", "*.*"),))],
              [sg.Text("Enter password"), sg.Input(key="-PASSWORD-", password_char="*")],
              [sg.Button("Submit"), sg.Button("Cancel")]]

    window = sg.Window("Retrieve a file", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Submit":
            youtube_link = values["-YOUTUBE_LINK-"]
            password = values["-PASSWORD-"]
            print(f"YouTube link: {youtube_link}")
            # print(f"Password: {password}")
            main_window["-TERMINAL-"].update(f"path to the video: {youtube_link}\ncreating file please wait...\n")
            window.close()

            handler = Handler(MainWindow=main_window)
            name = handler.retreive(youtube_link, password)
            main_window["-TERMINAL-"].update(f"path to the video: {youtube_link}\ncreating file please wait...\nfile saved as {name}")
            break

    window.close()

def main_window():
    sg.theme('LightGrey1')

    layout = [[sg.Image(filename="logo.png", size=(300, 300))],
              [sg.Button("Save a new file", size=(40, 2), key="-SAVE-")],
              [sg.Button("Retrieve an already saved file", size=(40, 2), key="-RETRIEVE-")],
              [sg.Multiline("", size=(80, 20), key="-TERMINAL-", pad=((0, 0), (100, 0)))]]
    global main_window
    main_window = sg.Window("Main Window", layout, element_justification="c", margins=(50, 50))

    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-SAVE-":
            save_file_window()
        elif event == "-RETRIEVE-":
            retrieve_file_window()
            

    main_window.close()

if __name__ == "__main__":
    main_window()
