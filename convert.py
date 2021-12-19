from PyQt6 import uic
with open('design.py', 'w', encoding="utf-8") as fout:      # dönüştürülecek ui dosyasına verilecek dosya adı
    uic.compileUi('design.ui', fout)     # ui dosyasını seç