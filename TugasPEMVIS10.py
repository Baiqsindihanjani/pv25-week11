import sys
import sqlite3
import csv
from PyQt5.QtWidgets import *


class FilmApp(QMainWindow):

    def init_db(self):
        self.conn = sqlite3.connect("film.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS film (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                genre TEXT,
                tahun TEXT
            )
        """)
        self.conn.commit()
        self.load_data()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Film Favorit")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Data Film")
        self.tabs.addTab(self.tab2, "Ekspor")

        self.tab1.setStyleSheet("background-color: #a9cce3;")
        self.tab2.setStyleSheet("background-color: #a9cce3;")

        self.create_menu()
        self.create_tab1()
        self.create_tab2()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

        self.infoLabel = QLabel("Nama: Baiq Sindi Hanjani | NIM: F1D022115")
        self.infoLabel.setStyleSheet("color: white; font-size: 12pt; background-color: #2c3e50; padding: 5px; border-radius: 5px;")
        main_layout.addWidget(self.infoLabel)

        self.central_widget.setLayout(main_layout)
        self.init_db()

        self.init_db()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        
        simpan_action = QAction("Simpan", self)
        simpan_action.triggered.connect(self.simpan_data)

        ekspor_action = QAction("Ekspor ke CSV", self)
        ekspor_action.triggered.connect(self.export_ke_csv)

        keluar_action = QAction("Keluar", self)
        keluar_action.triggered.connect(self.close)

        file_menu.addAction(simpan_action)
        file_menu.addAction(ekspor_action)
        file_menu.addAction(keluar_action)

        edit_menu = menubar.addMenu("Edit")
        
        cari_action = QAction("Cari Judul", self)
        cari_action.triggered.connect(self.fokus_cari_judul)

        hapus_action = QAction("Hapus Data", self)
        hapus_action.triggered.connect(self.hapus_data)

        edit_menu.addAction(cari_action)
        edit_menu.addAction(hapus_action)

    def create_tab1(self):
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Judul:"))
        self.judul_input = QLineEdit()
        self.judul_input.setStyleSheet("background-color: white;")
        row1.addWidget(self.judul_input)
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Genre:"))
        self.genre_input = QLineEdit()
        self.genre_input.setStyleSheet("background-color: white;")
        row2.addWidget(self.genre_input)
        form_layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Tahun:"))
        self.tahun_input = QLineEdit()
        self.tahun_input.setStyleSheet("background-color: white;")
        row3.addWidget(self.tahun_input)
        form_layout.addLayout(row3)

        self.save_button = QPushButton("Simpan")
        self.save_button.clicked.connect(self.simpan_data)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari judul...")
        self.search_input.setStyleSheet("background-color: white;")
        self.search_input.textChanged.connect(self.cari_data)
        layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Genre", "Tahun"])
        self.table.setStyleSheet("background-color: white;")
        layout.addWidget(self.table)

        self.table.cellDoubleClicked.connect(self.edit_data)

        self.delete_button = QPushButton("Hapus Data")
        self.delete_button.clicked.connect(self.hapus_data)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """)
        layout.addWidget(self.delete_button)

        self.tab1.setLayout(layout)
    
    def create_tab2(self):
        layout = QVBoxLayout()

        self.label_export = QLabel("Export Data ke CSV")
        self.export_button = QPushButton("Export ke CSV")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """)
        self.export_button.clicked.connect(self.export_ke_csv)

        layout.addWidget(self.label_export)
        layout.addWidget(self.export_button)
        layout.addStretch()

        self.tab2.setLayout(layout)

    def simpan_data(self):
        judul = self.judul_input.text()
        genre = self.genre_input.text()
        tahun = self.tahun_input.text()

        if judul and genre and tahun:
            self.cursor.execute("INSERT INTO film (judul, genre, tahun) VALUES (?, ?, ?)",
                                (judul, genre, tahun))
            self.conn.commit()
            self.load_data()
            self.judul_input.clear()
            self.genre_input.clear()
            self.tahun_input.clear()

    def load_data(self):
        self.table.setRowCount(0)
        self.cursor.execute("SELECT * FROM film")
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def cari_data(self, text):
        query = f"SELECT * FROM film WHERE judul LIKE ?"
        self.cursor.execute(query, ('%' + text + '%',))
        hasil = self.cursor.fetchall()

        self.table.setRowCount(0)
        for row_index, row_data in enumerate(hasil):
            self.table.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def hapus_data(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            id_item = self.table.item(selected_row, 0)
            if id_item:
                id_film = int(id_item.text())
                self.cursor.execute("DELETE FROM film WHERE id=?", (id_film,))
                self.conn.commit()
                self.load_data()

    def edit_data(self, row, column):
        id_item = self.table.item(row, 0)
        if not id_item:
            return
        film_id = int(id_item.text())

        kolom_map = {1: ("judul", "Judul"),
                     2: ("genre", "Genre"),
                     3: ("tahun", "Tahun")}
        if column not in kolom_map:
            return

        db_name, label = kolom_map[column]
        old_value = self.table.item(row, column).text()

        baru, ok = QInputDialog.getText(
            self, f"Edit {label}", f"{label}:",
            text=old_value
        )
        if ok and baru and baru != old_value:
            self.cursor.execute(
                f"UPDATE film SET {db_name} = ? WHERE id = ?",
                (baru, film_id)
            )
            self.conn.commit()
            self.load_data()

    def export_ke_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", "CSV Files (*.csv)")
        if path:
            self.cursor.execute("SELECT * FROM film")
            data = self.cursor.fetchall()

            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Judul", "Genre", "Tahun"])
                writer.writerows(data)

            QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke CSV.")
    
    def fokus_cari_judul(self):
        self.tabs.setCurrentWidget(self.tab1)
        self.search_input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmApp()
    window.show()
    sys.exit(app.exec_())