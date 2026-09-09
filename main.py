import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import pygame

# Import logic evaluasi matematika yang sudah dipisah
from logic import evaluate_expression

# Import mapping dari setup_assets
try:
    from setup_assets import BUTTON_MAPPING
except ImportError:
    BUTTON_MAPPING = {}

class KalkulatorPiano(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Scientific - Piano Theme")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #111111;") # Piano body color (dark)
        
        # Setup Pygame Mixer buat ngeluarin suara (pakai pygame biar delay-nya sekecil mungkin pas neken tombol)
        pygame.mixer.init()
        self.sounds = {}
        self.load_all_assets()
        
        self.init_ui()

    def load_all_assets(self):
        """Fungsi buat nge-load semua file .wav dari folder assets ke memory biar cepet dipanggil"""
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        if os.path.exists(assets_dir) and BUTTON_MAPPING:
            for btn_key, data in BUTTON_MAPPING.items():
                safe_name = data['safe_name']
                snd_path = os.path.join(assets_dir, f"snd_{safe_name}.wav")
                if os.path.exists(snd_path):
                    try:
                        self.sounds[btn_key] = pygame.mixer.Sound(snd_path)
                    except Exception as e:
                        print(f"Gagal memuat suara {snd_path}: {e}")
        else:
            print("Folder assets atau mapping tidak ditemukan. Jalankan setup_assets.py terlebih dahulu.")

    def play_sound(self, btn_key):
        """Fungsi buat muter suara sesuai tombol yang diklik/ditekan"""
        if btn_key in self.sounds:
            # Stop suara sebelumnya biar ngga numpuk berisik kalo diketik cepet-cepet
            pygame.mixer.stop()
            self.sounds[btn_key].play()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Layar output kalkulatornya (yang nampilin angka)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setFont(QFont("Arial", 24, QFont.Bold))
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #E6E6E6;
                color: #111111;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.display)
        
        # Grid Tombol
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)
        
        buttons = [
            ('sin(', 0, 0), ('cos(', 0, 1), ('tan(', 0, 2), ('log(', 0, 3),
            ('ln(', 1, 0), ('sqrt(', 1, 1), ('(', 1, 2), (')', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
            ('C', 6, 0, 1, 2), ('DEL', 6, 2), ('^', 6, 3)
        ]
        
        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            rowspan = btn[3] if len(btn) > 3 else 1
            colspan = btn[4] if len(btn) > 4 else 1
            
            button = QPushButton(text)
            button.setMinimumHeight(60)
            button.setFont(QFont("Arial", 16, QFont.Bold))
            button.setCursor(Qt.PointingHandCursor)
            
            # Styling tombol dengan gambar jika ada
            self.style_button(button, text)
            
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            grid_layout.addWidget(button, row, col, rowspan, colspan)

    def style_button(self, button, text):
        """Ngasih style CSS spesifik ke masing-masing tombol, sekalian nge-load gambarnya (kalo ada)"""
        base_style = """
            QPushButton {
                background-color: #34495e;
                color: white;
                border-radius: 10px;
                border: 2px solid #2c3e50;
            }
            QPushButton:hover { background-color: #415b76; }
            QPushButton:pressed { background-color: #2c3e50; }
        """
        
        if text in BUTTON_MAPPING:
            safe_name = BUTTON_MAPPING[text]['safe_name']
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
            img_path = os.path.join(assets_dir, f"img_{safe_name}.png")
            
            if os.path.exists(img_path):
                img_path = img_path.replace("\\", "/") # Fix Windows path format for QSS
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-image: url('{img_path}');
                        background-repeat: no-repeat;
                        background-position: center;
                        background-color: transparent;
                        color: transparent; /* Teks aslinya diumpetin aja soalnya udah ada di gambar */
                        border-radius: 10px;
                        border: 2px solid #ecf0f1;
                    }}
                    QPushButton:hover {{
                        border: 2px solid #666666;
                    }}
                    QPushButton:pressed {{
                        border: 2px solid #FFFFFF;
                        background-color: #333333;
                    }}
                """)
            else:
                button.setStyleSheet(base_style)
        else:
            button.setStyleSheet(base_style)

    def on_button_click(self, text):
        # Langsung bunyikan suaranya! 🎹
        self.play_sound(text)

        current_text = self.display.text()

        if text == 'C':
            self.display.clear()
        elif text == 'DEL':
            self.display.setText(current_text[:-1])
        elif text == '=':
            if current_text:
                result = evaluate_expression(current_text)
                self.display.setText(str(result))
        else:
            self.display.setText(current_text + text)

    def keyPressEvent(self, event):
        key = event.key()
        # Mapping dari tombol fisik keyboard ke fungsi tombol kalkulator
        key_mapping = {
            Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3', Qt.Key_4: '4',
            Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7', Qt.Key_8: '8', Qt.Key_9: '9',
            Qt.Key_Plus: '+', Qt.Key_Minus: '-', Qt.Key_Asterisk: '*', Qt.Key_Slash: '/',
            Qt.Key_Period: '.', Qt.Key_AsciiCircum: '^', Qt.Key_ParenLeft: '(', Qt.Key_ParenRight: ')',
            Qt.Key_Enter: '=', Qt.Key_Return: '=', Qt.Key_Equal: '=',
            Qt.Key_Backspace: 'DEL', Qt.Key_Delete: 'C', Qt.Key_Escape: 'C'
        }
        
        if key in key_mapping:
            self.on_button_click(key_mapping[key])
        else:
            # Kalo tombol lain yang dipencet, lempar lagi ke sistem Qt-nya
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Cek dulu, kalau folder assets-nya kosong atau kurang isinya, kita trigger script setup otomatis
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    if not os.path.exists(assets_dir) or len(os.listdir(assets_dir)) < 20: 
        print("Waduh, gambar & suara belum lengkap. Bentar, digenerate dulu otomatis...")
        try:
            import setup_assets
            setup_assets.main()
        except Exception as e:
            print(f"Yah gagal generate aset nih, errornya: {e}")

    window = KalkulatorPiano()
    window.show()
    sys.exit(app.exec_())
