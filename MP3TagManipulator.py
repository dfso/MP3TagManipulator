import sys
import os

import taglib


from PySide2.QtWidgets import (
    QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QFileSystemModel,
    QTreeView, QCheckBox
)


class MP3TagManipulator(QWidget):
    last_directory = '.'
    song = None
    def __init__(self):
        super().__init__()
        self.title = 'MP3TagManipulator v1.0'
        self.top = 100
        self.left = 100
        self.height = 400
        self.width = 640

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        # layout root of application
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # to set the model of tree
        model = QFileSystemModel()
        model.setRootPath("/home/denison/Downloads/music")
        model.setNameFilters(['*.mp3', '*.m4a', '*.flac'])
        model.setNameFilterDisables(False)

        self.tree = QTreeView()
        self.tree.setModel(model)
        self.tree.setAnimated(True)
        self.tree.setColumnWidth(0, 500)

        file_layout = QHBoxLayout()
        label_file = QLabel('file/directory')
        text_file = QLineEdit()
        btn_load = QPushButton('load')
        file_layout.addWidget(label_file)
        file_layout.addWidget(text_file)
        file_layout.addWidget(btn_load)

        grid_info_layout = QGridLayout()
        # strings to labels
        self.labels = ['ARTIST', 'ALBUMARTIST', 'ALBUM', 'TITLE', 'GENRE', 'DATE']

        # line edits to tags
        self.text_artist = QLineEdit('ARTIST')
        self.text_album = QLineEdit('ALBUM')
        self.text_album_artist = QLineEdit('ALBUMARTIST')
        self.text_title = QLineEdit('TITLE')
        self.text_genre = QLineEdit('GENRE')
        self.text_date = QLineEdit('DATE')

        self.text_tags = [
            self.text_artist, self.text_album_artist, self.text_album,
            self.text_title, self.text_genre, self.text_date
        ]

        for text in self.text_tags:
            text.setEnabled(False)
            #text.textChanged.connect(self.enable_save)

        # labels
        for label, i in zip(self.labels, range(6)):
            grid_info_layout.addWidget(QLabel(label), i, 0)

        # cb_artist = QCheckBox()
        # cb_album_artist = QCheckBox()
        # cb_album = QCheckBox()
        # cb_title = QCheckBox()
        # cb_genre = QCheckBox()
        # cb_date = QCheckBox()
        # self.checkboxes = [
        #     cb_artist, cb_album_artist, cb_album,
        #     cb_title, cb_genre, cb_date
        # ]

        # for cb in self.checkboxes:
        #     cb.setText('editar')

        # cb_artist.stateChanged.connect(lambda: self.enable_tag_edit(self.text_artist))
        # cb_album_artist.stateChanged.connect(lambda: self.enable_tag_edit(self.text_album_artist))
        # cb_album.stateChanged.connect(lambda: self.enable_tag_edit(self.text_album))
        # cb_title.stateChanged.connect(lambda: self.enable_tag_edit(self.text_title))
        # cb_genre.stateChanged.connect(lambda: self.enable_tag_edit(self.text_genre))
        # cb_date.stateChanged.connect(lambda: self.enable_tag_edit(self.text_date))

        for i, text in zip(range(6), self.text_tags):
            grid_info_layout.addWidget(text, i, 1)

        # for cb, i in zip(self.checkboxes, range(6)) :
        #     grid_info_layout.addWidget(cb, i, 2)

        action_layout = QHBoxLayout()
        btn_exit = QPushButton('Exit')
        self.btn_save = QPushButton('save changes')
        self.btn_save.setDisabled(True)
        action_layout.addWidget(btn_exit)
        action_layout.addWidget(self.btn_save)

        #main_layout.addLayout(file_layout)
        main_layout.addWidget(self.tree)
        main_layout.addLayout(grid_info_layout)
        main_layout.addLayout(action_layout)

        btn_load.clicked.connect(self.open_file)
        btn_exit.clicked.connect(self.close_application)
        self.btn_save.clicked.connect(self.edit_tags)
        self.tree.doubleClicked.connect(self.get_selected_file)
        self.show()

    def enable_edit_text(self):
        if self.song:
            for t in self.text_tags:
                t.setEnabled(True)
            self.enable_save()
        else:
            for t in self.text_tags:
                t.setEnabled(False)


    def enable_save(self):
        self.btn_save.setEnabled(True)

    def close_application(self):
        if self.song:
            self.song.close()
        print('vazando...;-)')
        self.close()

    def enable_tag_edit(self, txt_edit):
        txt_edit.setEnabled(not txt_edit.isEnabled())
        for edit in self.text_tags:
            edit.textChanged.connect(self.enable_save)
        print('executou self.enable_tag_edit()')
        print('não sei o q tá acontecendo :(')

    def get_selected_file(self):
        print('executou self.get_selected_file()')
        selected = self.tree.selectedIndexes()[0]
        print(selected.model().filePath(selected))
        self.song = taglib.File(selected.model().filePath(selected))
        self.enable_edit_text()
        self.load_song_info(self.song)
        return self.song

    def edit_tags(self):
        print("não tá funcionando 8'-(")
        self.song.tags['ARTIST'] = self.text_artist.text()
        self.song.tags['ALBUMARTIST'] = self.text_album_artist.text()
        self.song.tags['ALBUM'] = self.text_album.text()
        self.song.tags['TITLE'] = self.text_title.text()
        self.song.tags['GENRE'] = self.text_genre.text()
        self.song.tags['DATE'] = self.text_date.text()
        self.song.save()
        print(self.song.tags)
        self.btn_save.setDisabled(True)
        self.song.close()

    def open_file(self):
        print('*** quase lá *** ')
        dialog = QFileDialog(self)
        dialog.setViewMode(QFileDialog.Detail)
        file = dialog.getOpenFileName(self, 'load...', self.last_directory, 'songs (*.mp3 *.m4a *.flac *.wma)')
        song = taglib.File(file[0])
        # print(song.tags)
        self.show_song_info(song)
        song.close()

    def load_song_info(self, song):
        print('executou self.load_song_info()')
        for t, tag in zip(self.text_tags, self.labels):
            try:
                t.setText(song.tags[tag][0])
            except KeyError:
                t.setText('none')
        #song.close()
        # for cb in self.checkboxes:
        #     cb.setChecked(False)

if __name__ == "__main__":
    app = QApplication([])
    widget = MP3TagManipulator()
    sys.exit(app.exec_())
