import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QTextEdit, QFileDialog, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QSplitter,
                             QTabWidget)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
import csv
import folium
import tempfile

class NMEAParserGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Ana pencere ayarları
        self.setWindowTitle('NMEA Parser - GPS Veri İşleyici')
        self.setGeometry(100, 100, 1200, 800) 
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Başlık
        title = QLabel('NMEA GPS Veri İşleyici')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)
        
        # Dosya seçme bölümü
        file_layout = QHBoxLayout()
        self.file_label = QLabel('Dosya seçilmedi')
        self.file_button = QPushButton('NMEA Dosyası Seç')
        self.file_button.clicked.connect(self.select_file)
        file_layout.addWidget(QLabel('Dosya:'))
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)
        
        # İşlem butonları
        button_layout = QHBoxLayout()
        self.process_button = QPushButton('Verileri İşle')
        self.process_button.clicked.connect(self.process_data)
        self.process_button.setEnabled(False)
        
        self.save_button = QPushButton('CSV Olarak Kaydet')
        self.save_button.clicked.connect(self.save_csv)
        self.save_button.setEnabled(False)
        
        self.clear_button = QPushButton('Temizle')
        self.clear_button.clicked.connect(self.clear_data)
        
        self.show_map_button = QPushButton('Haritada Göster')
        self.show_map_button.clicked.connect(self.show_map)
        self.show_map_button.setEnabled(False)
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.show_map_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        
        # Ana içerik için splitter (bölme)
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Sol panel - Veri tablosu
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        left_layout.addWidget(QLabel('GPS Verileri'))
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Enlem (Latitude)', 'Boylam (Longitude)', 'Yükseklik (Altitude)'])
        
        # Başlangıç sütun genişliklerini ayarla
        self.table.setColumnWidth(0, 150)  # Enlem sütunu
        self.table.setColumnWidth(1, 150)  # Boylam sütunu  
        self.table.setColumnWidth(2, 120)  # Yükseklik sütunu
        
        left_layout.addWidget(self.table)
        splitter.addWidget(left_widget)
        
        # Sağ panel - Harita görünümü
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        right_layout.addWidget(QLabel('Harita Görünümü'))
        self.map_view = QWebEngineView()
        self.map_view.setMinimumWidth(400)
        right_layout.addWidget(self.map_view)
        splitter.addWidget(right_widget)

        # Splitter oranları (48% tablo, 52% harita)
        splitter.setStretchFactor(0, 48)
        splitter.setStretchFactor(1, 52)

        # Durum bilgisi
        self.status_label = QLabel('Hazır - Lütfen bir NMEA dosyası seçin')
        layout.addWidget(self.status_label)
        
        # Veriler için değişken
        self.processed_data = []
        self.selected_file = None
        
        # Varsayılan harita yükle
        self.load_default_map()
        
    def select_file(self):
        """Dosya seçme fonksiyonu"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'NMEA Dosyası Seç', 
            '', 
            'NMEA Files (*.nmea);;NMEA Files (*.txt);;CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.process_button.setEnabled(True)
            self.status_label.setText(f'Dosya seçildi: {os.path.basename(file_path)}')
    
    def process_data(self):
        """NMEA verilerini işleme fonksiyonu"""
        if not self.selected_file:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen önce bir dosya seçin!')
            return
        
        try:
            # Dosya uzantısını kontrol et
            file_extension = os.path.splitext(self.selected_file)[1].lower()
            
            if file_extension == '.csv':
                # CSV dosyasını işle
                self.process_csv_file()
            else:
                # NMEA dosyasını işle
                self.process_nmea_file()
                
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Veri işleme sırasında hata: {str(e)}')
            print(f"Genel hata: {e}")
    
    def process_csv_file(self):
        """CSV dosyasını işleme fonksiyonu"""
        try:
            self.processed_data = []
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader, None)  # İlk satırı (başlıkları) atla
                
                for row in csv_reader:
                    if len(row) >= 3:
                        try:
                            lat = float(row[0])
                            lon = float(row[1])
                            alt = float(row[2])
                            self.processed_data.append([lat, lon, alt])
                        except ValueError:
                            continue
            
            # Tabloyu güncelle
            self.update_table()
            
            # Durum bilgisini güncelle
            self.status_label.setText(f'CSV dosyasından {len(self.processed_data)} veri yüklendi')
            self.save_button.setEnabled(True)
            self.show_map_button.setEnabled(True)  # Harita butonunu aktif et
            
            QMessageBox.information(
                self, 
                'Başarılı', 
                f'{len(self.processed_data)} adet veri CSV dosyasından yüklendi!'
            )
            
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'CSV dosyası okuma hatası: {str(e)}')
    
    def process_nmea_file(self):
        """NMEA dosyasını işleme fonksiyonu"""
        import subprocess
        import tempfile
        import shutil
        
        try:
            # Geçici bir kopyasını oluştur ve data.txt olarak kaydet
            temp_dir = tempfile.mkdtemp()
            temp_data_file = os.path.join(temp_dir, 'data.txt')
            shutil.copy2(self.selected_file, temp_data_file)
            
            # nmea.py'yi geçici klasörde çalıştır
            nmea_script_path = os.path.join(os.path.dirname(self.selected_file), 'nmea.py')
            if not os.path.exists(nmea_script_path):
                nmea_script_path = os.path.join(os.path.dirname(__file__), 'nmea.py')
            
            # nmea.py'yi kopyala
            temp_nmea_file = os.path.join(temp_dir, 'nmea.py')
            shutil.copy2(nmea_script_path, temp_nmea_file)
            
            # nmea.py'yi çalıştır
            result = subprocess.run(
                ['python3', 'nmea.py'], 
                cwd=temp_dir,
                capture_output=True, 
                text=True
            )
            
            # Oluşturulan CSV dosyasını oku
            csv_output_path = os.path.join(temp_dir, 'nmea_output.csv')
            if os.path.exists(csv_output_path):
                self.processed_data = []
                with open(csv_output_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    headers = next(csv_reader, None)  # Başlıkları atla
                    
                    for row in csv_reader:
                        if len(row) >= 3:
                            try:
                                lat = float(row[0])
                                lon = float(row[1])
                                alt = float(row[2])
                                self.processed_data.append([lat, lon, alt])
                            except ValueError:
                                continue
                
                # Tabloyu güncelle
                self.update_table()
                
                # Durum bilgisini güncelle
                valid_count = len(self.processed_data)
                self.status_label.setText(f'İşlendi: {valid_count} geçerli GGA cümlesi')
                self.save_button.setEnabled(True)
                self.show_map_button.setEnabled(True)  # Harita butonunu aktif et
                
                if valid_count > 0:
                    QMessageBox.information(
                        self, 
                        'Başarılı', 
                        f'{valid_count} adet GGA cümlesi başarıyla işlendi!\n'
                        f'nmea.py scripti çalıştırılarak veriler işlendi.'
                    )
                else:
                    QMessageBox.warning(
                        self, 
                        'Uyarı', 
                        'Hiç geçerli GGA cümlesi bulunamadı!'
                    )
            else:
                QMessageBox.warning(
                    self, 
                    'Uyarı', 
                    'nmea.py çalıştırıldı ancak CSV dosyası oluşturulamadı!\n'
                    f'Script çıktısı: {result.stdout}\n'
                    f'Hata: {result.stderr}'
                )
            
            # Geçici dosyaları temizle
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                'Hata', 
                f'nmea.py çalıştırılırken hata oluştu: {str(e)}'
            )
    
    def update_table(self):
        """Tabloyu güncelleme fonksiyonu"""
        self.table.setRowCount(len(self.processed_data))
        
        for row, data in enumerate(self.processed_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)
        
        # Sütun genişliklerini ayarla
        self.table.resizeColumnsToContents()
        
        # Minimum sütun genişliklerini belirle
        self.table.setColumnWidth(0, max(150, self.table.columnWidth(0)))  # Enlem için minimum 150px
        self.table.setColumnWidth(1, max(150, self.table.columnWidth(1)))  # Boylam için minimum 150px
        self.table.setColumnWidth(2, max(120, self.table.columnWidth(2)))  # Yükseklik için minimum 120px
    
    def load_default_map(self):
        """Varsayılan haritayı yükler"""
        try:
            # Dünya haritası oluştur
            m = folium.Map(location=[39.9334, 32.8597], zoom_start=6)  # Türkiye merkezi
            
            # Geçici dosya oluştur
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            m.save(temp_file.name)
            
            # Haritayı web view'e yükle
            self.map_view.load(QUrl.fromLocalFile(temp_file.name))
            
        except Exception as e:
            print(f"Varsayılan harita yükleme hatası: {e}")
    
    def show_map(self):
        """GPS verilerini haritada göster"""
        if not self.processed_data:
            QMessageBox.warning(self, 'Uyarı', 'Gösterilecek GPS verisi yok!')
            return
        
        try:
            # Koordinatların ortalamasını hesapla (harita merkezi için)
            avg_lat = sum(data[0] for data in self.processed_data) / len(self.processed_data)
            avg_lon = sum(data[1] for data in self.processed_data) / len(self.processed_data)
            
            # Harita oluştur
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
            
            # Her GPS noktası için marker ekle
            for i, (lat, lon, alt) in enumerate(self.processed_data):
                folium.Marker(
                    [lat, lon],
                    popup=f'Nokta {i+1}<br>Enlem: {lat}<br>Boylam: {lon}<br>Yükseklik: {alt}m',
                    tooltip=f'Nokta {i+1}'
                ).add_to(m)
            
            # Eğer birden fazla nokta varsa, rota çiz
            if len(self.processed_data) > 1:
                coordinates = [[data[0], data[1]] for data in self.processed_data]
                folium.PolyLine(
                    coordinates,
                    color='red',
                    weight=3,
                    opacity=0.8,
                    popup='GPS Rotası'
                ).add_to(m)
            
            # Geçici dosya oluştur ve kaydet
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            m.save(temp_file.name)
            
            # Haritayı web view'e yükle
            self.map_view.load(QUrl.fromLocalFile(temp_file.name))
            
            QMessageBox.information(
                self, 
                'Başarılı', 
                f'{len(self.processed_data)} GPS noktası haritada gösterildi!'
            )
            
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Harita oluşturma hatası: {str(e)}')
    
    def save_csv(self):
        """CSV dosyası kaydetme fonksiyonu"""
        if not self.processed_data:
            QMessageBox.warning(self, 'Uyarı', 'Kaydedilecek veri yok!')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            'CSV Dosyası Kaydet', 
            'nmea_output.csv', 
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["latitude", "longitude", "altitude"])
                    writer.writerows(self.processed_data)
                
                QMessageBox.information(
                    self, 
                    'Başarılı', 
                    f'Veriler başarıyla kaydedildi:\n{file_path}'
                )
                self.status_label.setText(f'CSV kaydedildi: {os.path.basename(file_path)}')
                
            except Exception as e:
                QMessageBox.critical(self, 'Hata', f'Dosya kaydetme hatası: {str(e)}')
    
    def clear_data(self):
        """Verileri temizleme fonksiyonu"""
        self.table.setRowCount(0)
        self.processed_data = []
        self.selected_file = None
        self.file_label.setText('Dosya seçilmedi')
        self.process_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.show_map_button.setEnabled(False)  # Harita butonunu deaktif et
        self.status_label.setText('Temizlendi - Lütfen bir NMEA dosyası seçin')
        
        # Varsayılan haritayı yeniden yükle
        self.load_default_map()

def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    
    # Uygulama stilini ayarla
    app.setStyle('Fusion')
    
    # Ana pencereyi oluştur ve göster
    window = NMEAParserGUI()
    window.show()
    
    # Uygulamayı çalıştır
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()