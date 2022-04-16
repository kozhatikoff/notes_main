from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QApplication,QWidget,QPushButton,QLabel,QVBoxLayout,QMessageBox,QRadioButton,QHBoxLayout,QListWidget,QLineEdit,QTextEdit,QFileDialog
import json

#создание окна
App=QApplication([])
notes_win=QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900,600)
#создание словаря и тегов
notes={
    'Добро пожаловать':{
        "текст":"это самое лучшее прииложение для создания заметок!",
        "теги":("добро","инструкция")
    }
}
with open("notes_data.json","w") as file:
    json.dump(notes,file)

#заметки
list_notes=QListWidget()
list_notes_label=QLabel("Список заметок")
button_note_create=QPushButton("Создать заметку")
button_note_del=QPushButton("Удалить заметку")
button_note_save=QPushButton("Сохранить заметку")
#теги
list_tag=QListWidget()
list_tag_label=QLabel("Список тегов ")
tag_line=QLineEdit(" ")
tag_line.setPlaceholderText("Введите тег")
button_tag_add=QPushButton("Добавить к заметке")
button_tag_del=QPushButton("Удалить тег ")
button_tag_search=QPushButton("Найти тег")
#создание окна для записи заметок
field_text=QTextEdit()
field_text.setText("Текст заметки                                          ")
#создание лейтаутов
col_1=QVBoxLayout()
col_1.addWidget(list_notes_label)
col_1.addWidget(list_notes)
col_1.addWidget(button_note_create)
col_1.addWidget(button_note_del)
col_1.addWidget(button_note_save)
col_1.addWidget(list_tag_label)
col_1.addWidget(list_tag)
col_1.addWidget(tag_line)
col_1.addWidget(button_tag_add)
col_1.addWidget(button_tag_del)
col_1.addWidget(button_tag_search)
col_2=QVBoxLayout()
col_2.addWidget(field_text)
layout_notes=QHBoxLayout()
layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)
notes_win.setLayout(layout_notes)
#ФУНКЦИОНАЛ ПРИЛОЖЕНИЯ
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tag.clear()
    list_tag.addItems(notes[key]["теги"])
def add_note():
    note_name, Ok=QInputDialog.getText(notes_win,"Добавить заметку","Название заметки")
    if Ok and note_name != "":
        notes[note_name]={'текст':"","теги":[]}
        list_notes.addItem(note_name)
        list_tag.addItems(notes[note_name]['теги'])
        print(notes)
button_note_create.clicked.connect(add_note)
def del_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tag.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json',"w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)


button_note_del.clicked.connect(del_note)
def save_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        notes[key]['текст']=field_text.toPlainText()
        with open('notes_data.json',"w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
    else:
        print(" ")
button_note_save.clicked.connect(save_note)
def add_tag():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=tag_line.text()
    if not tag in notes[key]['теги']:
        notes[key]["теги"].append(tag)
        list_tag.addItem(tag)
        with open('notes_data.json',"w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
button_tag_add.clicked.connect(add_tag)
def del_tag():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=tag_line.text()
        notes[key]["теги"].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]['теги'])
        with open('notes_data.json',"w")as file:
            json.dump(notes,file,sort_keys=True,ensure_ascii=False)
button_tag_del.clicked.connect(del_tag)
def search_tag():
    tag=tag_line.text()
    if button_tag_search.text()=='Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if  tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text()=="Сбросить поиск":
        tag_line.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")
    else:
        pass
button_tag_search.clicked.connect(search_tag)








button_note_create.clicked.connect(save_note)




'''запуск приложения'''
#подключение обработки событий
list_notes.itemClicked.connect(show_note)

#запуск приложения
notes_win.show()

with open('notes_data.json',"r") as file:
    notes=json.load(file)
list_notes.addItems(notes)
App.exec()