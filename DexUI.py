# DexUI.py 
#
from PyQt6.QtWidgets import (
    QApplication, QDialog, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget,
    QVBoxLayout, QWidget
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import requests
import sys
from pokeapi.fetch import get_pokemon_data

# Create main UI Window
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pokedex")                          # Window Title

        self.setMinimumSize(600,550)                            # Window Size
        self.setMaximumSize(600,550)

        self.name_label = QLabel("Name/ID:")
        self.name_value_label = QLabel("")                      # Label filled w/ self.name_value_label.setText()
        self.create_top_left_group()                            # Initialize Groups
        self.create_top_right_group()
        self.create_bottom_left_tabs()
        self.create_bottom_right_group()

        self.setup_layout()
        self.search_button.clicked.connect(self.handle_search)  # Handle Search

    def setup_layout(self):
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.name_label)
        top_layout.addWidget(self.name_value_label)
        top_layout.addStretch(1)

        main_layout = QGridLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)          # Margins
        main_layout.setHorizontalSpacing(15)
        main_layout.setVerticalSpacing(15)

        main_layout.addLayout(top_layout, 0, 0, 1, 2)
        main_layout.addWidget(self.top_left_group, 1, 0)
        main_layout.addWidget(self.top_right_group, 1, 1)
        main_layout.addWidget(self.bottom_left_tabs, 2, 0)
        main_layout.addWidget(self.bottom_right_group, 2, 1)

        main_layout.setRowStretch(0, 0)
        main_layout.setRowStretch(1, 0)
        main_layout.setRowStretch(2, 0)
        main_layout.setColumnStretch(0, 0)
        main_layout.setColumnStretch(1, 1)

        self.setLayout(main_layout)

    # Sprite Display Section
    def create_top_left_group(self):
        self.top_left_group = QGroupBox(" Sprite ")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(QPixmap("Resources/poke_ball.png"))
        self.image_label.setFixedSize(96, 96)                   # Default Sprite Size from repo
        self.image_label.setScaledContents(True)                # Scale Image for correct aspect ratio

        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center in section
        self.top_left_group.setLayout(layout)


    # Update image from default
    def update_sprite_image(self, url: str):
        try:
            response = requests.get(url)
            image = QImage()
            if image.loadFromData(response.content):
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap)
            else:
                print("Failed to load image data from URL.")
        except Exception as e:
            print(f"Error loading image from URL: {e}")

    # Information Section
    def create_top_right_group(self):
        self.top_right_group = QGroupBox(" Information ")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.info_label = QLabel("Pokémon info will appear here.")
        layout.addWidget(self.info_label)
        layout.addStretch(1)
        self.top_right_group.setLayout(layout)

    # Stats table(s) section
    def create_bottom_left_tabs(self):
        self.bottom_left_tabs = QTabWidget()
        base_stats_tab = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.stats_table = QTableWidget(6, 2)
        self.stats_table.setFixedSize(220, 210)
        self.stats_table.setHorizontalHeaderLabels(["Stat", "Value"])
        layout.addWidget(self.stats_table)

        base_stats_tab.setLayout(layout)
        self.bottom_left_tabs.addTab(base_stats_tab, "Base Stats")

    def populate_stats_table(self, stats: dict):
        self.stats_table.setRowCount(len(stats))
        for row, (stat_name, value) in enumerate(stats.items()):
            self.stats_table.setItem(row, 0, QTableWidgetItem(stat_name))
            self.stats_table.setItem(row, 1, QTableWidgetItem(str(value)))

    # Search Section
    def create_bottom_right_group(self):
        self.bottom_right_group = QGroupBox(" Search ")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter Name or National Dex #')
        self.search_button = QPushButton("Search")
        self.search_button.setDefault(True)

        self.fun_fact_label = QLabel(f"\nFun Fact:")
        self.fun_fact_label.setWordWrap(True)

        layout.addWidget(self.search_input)                         # Search Bar
        layout.addWidget(self.search_button)                        # Search Button
        layout.addWidget(self.fun_fact_label)                       # Fun Fact
        layout.addStretch(1)

        self.bottom_right_group.setLayout(layout)

    # Query function for search button
    def handle_search(self):
        query = self.search_input.text().strip()
        if not query:
            return
        # Logic from app.py
        try:
            data = get_pokemon_data(query)
            self.update_sprite_image(data.get("sprite_url", "")) # Update Image from (sprite) response URL 
            self.populate_stats_table(data.get("stats", {}))     # Fill Base Stats table

            # Populate Information
            self.name_value_label.setText(f"#{data.get('id', '?')} - {data.get('name', 'Unknown')}")    # Name Label Pop
            self.info_label.setText(
                f"Type(s): {', '.join(data.get('types', []))}\n"
                f"Abilities: {', '.join(data.get('abilities', []))}\n"
                f"Generation: {data.get('generation', 'Unknown').upper()}"
            )
            self.fun_fact_label.setText(f"\nFun Fact: {data.get('fun_fact', 'N/A')}")

        except Exception as e:
            self.name_value_label.setText("")
            self.info_label.setText(f"Error: {e}")
            self.fun_fact_label.setText("\nFun Fact: N/A")
            print(f"Search error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
