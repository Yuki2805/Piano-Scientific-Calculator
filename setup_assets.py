import os
import wave
import struct
import math
import sys

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QImage, QPainter, QColor, QFont
    from PyQt5.QtCore import Qt, QRect
    has_pyqt = True
except ImportError:
    has_pyqt = False

# ==========================================
# Konfigurasi Tuts Piano 🎹
# ==========================================
# Idenya gini:
# - Angka (0-9) kita jadiin tuts putih (nada dasar mulai dari C4)
# - Operator & Fungsi matematika kita jadiin tuts hitam (nada kres/kres #)
BUTTON_MAPPING = {
    '1': {'safe_name': '1', 'text': '1', 'color': '#F5F5F5', 'freq': 261.63}, # C4
    '2': {'safe_name': '2', 'text': '2', 'color': '#F5F5F5', 'freq': 293.66}, # D4
    '3': {'safe_name': '3', 'text': '3', 'color': '#F5F5F5', 'freq': 329.63}, # E4
    '4': {'safe_name': '4', 'text': '4', 'color': '#F5F5F5', 'freq': 349.23}, # F4
    '5': {'safe_name': '5', 'text': '5', 'color': '#F5F5F5', 'freq': 392.00}, # G4
    '6': {'safe_name': '6', 'text': '6', 'color': '#F5F5F5', 'freq': 440.00}, # A4
    '7': {'safe_name': '7', 'text': '7', 'color': '#F5F5F5', 'freq': 493.88}, # B4
    '8': {'safe_name': '8', 'text': '8', 'color': '#F5F5F5', 'freq': 523.25}, # C5
    '9': {'safe_name': '9', 'text': '9', 'color': '#F5F5F5', 'freq': 587.33}, # D5
    '0': {'safe_name': '0', 'text': '0', 'color': '#F5F5F5', 'freq': 659.25}, # E5
    '=': {'safe_name': 'eq', 'text': '=', 'color': '#E0E0E0', 'freq': 698.46}, # F5
    'C': {'safe_name': 'clear', 'text': 'C', 'color': '#FFCCCC', 'freq': 783.99}, # G5
    'DEL': {'safe_name': 'del', 'text': 'DEL', 'color': '#FFCCCC', 'freq': 880.00}, # A5
    '+': {'safe_name': 'add', 'text': '+', 'color': '#2C3E50', 'freq': 277.18}, # C#4
    '-': {'safe_name': 'sub', 'text': '-', 'color': '#2C3E50', 'freq': 311.13}, # D#4
    '*': {'safe_name': 'mul', 'text': '*', 'color': '#2C3E50', 'freq': 369.99}, # F#4
    '/': {'safe_name': 'div', 'text': '/', 'color': '#2C3E50', 'freq': 415.30}, # G#4
    '.': {'safe_name': 'dot', 'text': '.', 'color': '#2C3E50', 'freq': 466.16}, # A#4
    '^': {'safe_name': 'pow', 'text': '^', 'color': '#2C3E50', 'freq': 554.37}, # C#5
    '(': {'safe_name': 'open_paren', 'text': '(', 'color': '#2C3E50', 'freq': 622.25}, # D#5
    ')': {'safe_name': 'close_paren', 'text': ')', 'color': '#2C3E50', 'freq': 739.99}, # F#5
    'sin(': {'safe_name': 'sin', 'text': 'sin(', 'color': '#1A252F', 'freq': 830.61}, # G#5
    'cos(': {'safe_name': 'cos', 'text': 'cos(', 'color': '#1A252F', 'freq': 932.33}, # A#5
    'tan(': {'safe_name': 'tan', 'text': 'tan(', 'color': '#1A252F', 'freq': 1108.73}, # C#6
    'log(': {'safe_name': 'log', 'text': 'log(', 'color': '#1A252F', 'freq': 1244.51}, # D#6
    'ln(': {'safe_name': 'ln', 'text': 'ln(', 'color': '#1A252F', 'freq': 1479.98}, # F#6
    'sqrt(': {'safe_name': 'sqrt', 'text': 'sqrt(', 'color': '#1A252F', 'freq': 1661.22}, # G#6
}

def create_beep_wav(filename, frequency=440.0, duration_ms=400):
    sample_rate = 44100
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Bikin suara ala synth sederhana (Sine wave murni dicampur dikit overtone)
            fundamental = math.sin(2.0 * math.pi * frequency * i / sample_rate)
            overtone = 0.3 * math.sin(2.0 * math.pi * (frequency * 2) * i / sample_rate)
            raw_val = fundamental + overtone
            
            # Efek fade out biar suaranya ngga putus tiba-tiba kayak robot wkwk
            envelope = math.exp(-3.0 * i / n_samples)
            
            value = int(32767.0 * 0.5 * raw_val * envelope)
            
            # Kliping untuk mencegah over-volume
            value = max(-32768, min(32767, value))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

def generate_image(filename, text, bg_color):
    if has_pyqt:
        if not QApplication.instance():
            app = QApplication(sys.argv)
            
        img = QImage(100, 100, QImage.Format_ARGB32)
        img.fill(QColor(bg_color))
        
        painter = QPainter(img)
        painter.setPen(QColor("#000000"))
        
        r = int(bg_color[1:3], 16)
        g = int(bg_color[3:5], 16)
        b = int(bg_color[5:7], 16)
        luminance = (0.299*r + 0.587*g + 0.114*b)
        if luminance < 128:
            painter.setPen(QColor("#FFFFFF"))
            
        font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, 100, 100), Qt.AlignCenter | Qt.TextWordWrap, text)
        painter.end()
        
        img.save(filename)
    else:
        print("Yah, PyQt5-nya belom di-install nih. Gambarnya gak bisa dibikin otomatis deh.")

def main():
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created directory: {assets_dir}")

    print("Lagi nyiapin gambar dan suara piano nih, tunggu bentar ya... 🎹")
    
    for btn_key, data in BUTTON_MAPPING.items():
        safe_name = data['safe_name']
        text = data['text']
        color = data['color']
        freq = data['freq']
        
        # Generate Piano Sound
        wav_path = os.path.join(assets_dir, f"snd_{safe_name}.wav")
        create_beep_wav(wav_path, frequency=freq, duration_ms=600) 
        
        # Generate Piano Key Image
        img_path = os.path.join(assets_dir, f"img_{safe_name}.png")
        generate_image(img_path, text, color)

    print("Mantap! Aset piano udah kelar digenerate semua. Gas mainkan!")

if __name__ == "__main__":
    main()
