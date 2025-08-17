import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QTextEdit, QFileDialog, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QSplitter,
                             QTabWidget, QComboBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
import csv
import folium
import tempfile
import subprocess
import shutil

class NMEAParserGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Main window settings
        self.setWindowTitle('NMEA Parser - GPS Data Processor')
        self.setGeometry(100, 100, 1200, 800) 
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        header_layout = QHBoxLayout()

        self.logo_label1 = QLabel()
        pixmap1 = QPixmap('logo.png')
        if not pixmap1.isNull():
            scaled_pixmap = pixmap1.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label1.setPixmap(scaled_pixmap)
        else:
            self.logo_label1.setText('LOGO')
            self.logo_label1.setStyleSheet("border: 1px solid gray; padding: 10px;")

        self.logo_label1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.logo_label1.setFixedSize(80, 80)

        self.logo_label2 = QLabel()
        pixmap2 = QPixmap('logo.png')
        if not pixmap2.isNull():
            scaled_pixmap = pixmap2.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label2.setPixmap(scaled_pixmap)
        else:
            self.logo_label2.setText('LOGO')
            self.logo_label2.setStyleSheet("border: 1px solid gray; padding: 10px;")

        self.logo_label2.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.logo_label2.setFixedSize(80, 80)

        # Title
        title = QLabel('NMEA GPS Data Processor')
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        layout.addWidget(title)

        header_layout.addWidget(self.logo_label1)
        header_layout.addWidget(title, 1)
        header_layout.addWidget(self.logo_label2)

        layout.addLayout(header_layout)

        # File selection section
        file_layout = QHBoxLayout()
        self.file_label = QLabel('No file selected')
        self.file_button = QPushButton('Select NMEA File')
        self.file_button.clicked.connect(self.select_file)
        file_layout.addWidget(QLabel('File:'))
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        layout.addLayout(file_layout)

        # Parser selection section
        parser_layout = QHBoxLayout()
        parser_layout.addWidget(QLabel('Parser Type:'))
        self.parser_combo = QComboBox()
        self.parser_combo.addItem("Default (GGA Parser)", "nmea_gga.py")
        self.parser_combo.addItem("GSA Parser", "nmea_gsa.py")
        self.parser_combo.addItem("GLL Parser", "nmea_gll.py")
        self.parser_combo.addItem("RMC Parser", "nmea_rmc.py")
        self.parser_combo.addItem("VTG Parser", "nmea_vtg.py")
        self.parser_combo.addItem("GSV Parser", "nmea_gsv.py")
        self.parser_combo.setEnabled(False)  # Initially disabled
        parser_layout.addWidget(self.parser_combo)
        layout.addLayout(parser_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        self.process_button = QPushButton('Process Data')
        self.process_button.clicked.connect(self.process_data)
        self.process_button.setEnabled(False)

        self.save_button = QPushButton('Save as CSV')
        self.save_button.clicked.connect(self.save_csv)
        self.save_button.setEnabled(False)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_data)

        self.show_map_button = QPushButton('Show on Map')
        self.show_map_button.clicked.connect(self.show_map)
        self.show_map_button.setEnabled(False)
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.show_map_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Left panel - Data table
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        left_layout.addWidget(QLabel('GPS Data'))
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.default_headers = ["Time of Fix(UTC)", 'Latitude', 'Longitude', 'Altitude', 'Number of Satellites', 'Fix Quality']
        self.table.setHorizontalHeaderLabels(self.default_headers)

        # Header alignment
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)

        # Set initial column widths
        self.table.setColumnWidth(0, 150)  # UTC column
        self.table.setColumnWidth(1, 150)  # Latitude column
        self.table.setColumnWidth(2, 150)  # Longitude column
        self.table.setColumnWidth(3, 150)  # Altitude column
        self.table.setColumnWidth(4, 150)  # Number of Satellites column
        self.table.setColumnWidth(5, 100)  # Fix Quality column
        
        left_layout.addWidget(self.table)
        splitter.addWidget(left_widget)

        # Right panel - Map view
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        right_layout.addWidget(QLabel('Map View'))
        self.map_view = QWebEngineView()
        self.map_view.setMinimumWidth(400)
        right_layout.addWidget(self.map_view)
        splitter.addWidget(right_widget)

        # Splitter ratios (49% table, 51% map)
        splitter.setStretchFactor(0, 49)
        splitter.setStretchFactor(1, 51)

        # Status information
        self.status_label = QLabel('Ready - Please select an NMEA file')
        layout.addWidget(self.status_label)

        # Variables for data
        self.processed_data = []
        self.selected_file = None

        # Load default map
        self.load_default_map()
        
    def select_file(self):
        """File selection function"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select NMEA File', 
            '', 
            'NMEA Files (*.nmea);;NMEA Files (*.txt);;CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.process_button.setEnabled(True)
            self.parser_combo.setEnabled(True)  # Enable parser selection
            self.status_label.setText(f'File selected: {os.path.basename(file_path)} - Please select a parser and process the data')

    def process_data(self):
        """NMEA data processing function"""
        if not self.selected_file:
            QMessageBox.warning(self, 'Warning', 'Please select a file first!')
            return
        
        try:
            # Check file extension
            file_extension = os.path.splitext(self.selected_file)[1].lower()
            
            if file_extension == '.csv':
                # Process CSV file
                self.process_csv_file()
            else:
                # Process NMEA file
                self.process_nmea_file()
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error during data processing: {str(e)}')
            print(f"General error: {e}")
    
    def process_csv_file(self):
        """CSV file processing function"""
        try:
            self.processed_data = []
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader, None)  # Skip the first row (headers)
                
                for row in csv_reader:
                    if len(row) >= 6:
                        try:
                            utc = row[0]  # Get UTC as string because it's formatted
                            lat = float(row[1])
                            lon = float(row[2])
                            alt = float(row[3])
                            satellites = int(row[4])
                            fix_quality = int(row[5])
                            self.processed_data.append([utc, lat, lon, alt, satellites, fix_quality])
                        except ValueError:
                            continue

            # Update table
            self.update_table()

            # Update status information
            self.status_label.setText(f'Loaded {len(self.processed_data)} records from CSV file')
            self.save_button.setEnabled(True)
            self.show_map_button.setEnabled(True)  # Enable map button
            
            QMessageBox.information(
                self,
                'Success',
                f'Loaded {len(self.processed_data)} records from CSV file!'
            )
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error reading CSV file: {str(e)}')

    def read_parser_csv_output(self, csv_path, parser_type):
        """Read CSV file according to parser type"""
        self.processed_data = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader, None)  # Get headers

                if parser_type == "nmea_gga.py":
                    # GGA parser - standard format
                    self.table.setColumnCount(6)
                    self.table.setHorizontalHeaderLabels(["Time of Fix(UTC)", 'Latitude', 'Longitude', 'Altitude', 'Number of Satellites', 'Fix Quality'])

                    for row in csv_reader:
                        if len(row) >= 6:
                            try:
                                utc = row[0]
                                lat = float(row[1])
                                lon = float(row[2])
                                alt = float(row[3])
                                satellites = int(row[4])
                                fix_quality = int(row[5])
                                self.processed_data.append([utc, lat, lon, alt, satellites, fix_quality])
                            except (ValueError, IndexError):
                                continue
                                
                elif parser_type == "nmea_gll.py":
                    # GLL parser 
                    self.table.setColumnCount(5)
                    self.table.setHorizontalHeaderLabels(["UTC Time", "Status", "Latitude", "Longitude", "Checksum"])
                    
                    for row in csv_reader:
                        if len(row) >= 5:
                            try:
                                self.processed_data.append([row[0], row[1], row[2], row[3], row[4]])
                            except IndexError:
                                continue
                                
                elif parser_type == "nmea_gsa.py":
                    # GSA parser
                    self.table.setColumnCount(6)
                    self.table.setHorizontalHeaderLabels(["Mode 1", "Mode 2", "Satellite IDs", "PDOP", "HDOP", "VDOP"])
                    
                    for row in csv_reader:
                        if len(row) >= 6:
                            try:
                                self.processed_data.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                            except IndexError:
                                continue
                                
                elif parser_type == "nmea_rmc.py":
                    # RMC parser
                    self.table.setColumnCount(10)
                    self.table.setHorizontalHeaderLabels(["utc_time", "status", "latitude", "longitude", "speed", "direction", "date", "magnetic_variation", "variation_direction", "checksum"])
                    
                    for row in csv_reader:
                        if len(row) >= 10:
                            try:
                                self.processed_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
                            except IndexError:
                                continue
                                
                elif parser_type == "nmea_vtg.py":
                    # VTG parser
                    self.table.setColumnCount(5)
                    self.table.setHorizontalHeaderLabels(["true_track", "magnetic_track", "speed_knots", "speed_kilometers", "checksum"])
                    
                    for row in csv_reader:
                        if len(row) >= 5:
                            try:
                                self.processed_data.append([row[0], row[1], row[2], row[3], row[4]])
                            except IndexError:
                                continue
                                
                elif parser_type == "nmea_gsv.py":
                    # GSV parser - simplified format
                    # Remove NMEA_Sentence and Total_GSV_Sentences columns
                    simplified_headers = []
                    if headers:
                        # Filter out unnecessary columns
                        for header in headers:
                            if header not in ["NMEA_Sentence", "Total_GSV_Sentences"]:
                                simplified_headers.append(header)
                        
                        self.table.setColumnCount(len(simplified_headers))
                        self.table.setHorizontalHeaderLabels(simplified_headers)
                    else:
                        # Fallback: simplified format
                        simplified_headers = ["Sentence_Number", "Satellites_in_View",
                                            "Sat_1_ID", "Sat_1_Elevation", "Sat_1_Azimuth", "Sat_1_SNR",
                                            "Sat_2_ID", "Sat_2_Elevation", "Sat_2_Azimuth", "Sat_2_SNR", 
                                            "Sat_3_ID", "Sat_3_Elevation", "Sat_3_Azimuth", "Sat_3_SNR",
                                            "Sat_4_ID", "Sat_4_Elevation", "Sat_4_Azimuth", "Sat_4_SNR",
                                            "Checksum"]
                        self.table.setColumnCount(len(simplified_headers))
                        self.table.setHorizontalHeaderLabels(simplified_headers)

                    # Process CSV data
                    for row in csv_reader:
                        if len(row) >= 5:
                            try:
                                # Remove unnecessary columns (NMEA_Sentence and Total_GSV_Sentences)
                                filtered_row = []
                                skip_indices = []
                                
                                if headers:
                                    # Determine which columns to skip
                                    for i, header in enumerate(headers):
                                        if header in ["NMEA_Sentence", "Total_GSV_Sentences"]:
                                            skip_indices.append(i)

                                    # Create filtered row
                                    for i, value in enumerate(row):
                                        if i not in skip_indices:
                                            filtered_row.append(value)
                                else:
                                    # Fallback: skip first 2 columns
                                    filtered_row = row[2:]

                                # Place checksum in the correct position - after the last filled satellite data
                                processed_row = []
                                checksum = ""

                                # Find and separate checksum
                                for i, value in enumerate(filtered_row):
                                    if isinstance(value, str) and value.startswith('*'):
                                        checksum = value
                                        break
                                    elif isinstance(value, str) and '*' in value:
                                        checksum = '*' + value.split('*')[1]
                                        filtered_row[i] = value.split('*')[0] if value.split('*')[0] else ''
                                        break

                                # Process row data
                                if len(filtered_row) >= 2:  # At least sentence_number and satellites_in_view
                                    processed_row.append(filtered_row[0])  # Sentence_Number
                                    processed_row.append(filtered_row[1])  # Satellites_in_View

                                    # Process satellite data (in groups of 4)
                                    satellite_data = filtered_row[2:]

                                    # Prepare fields for 4 satellites
                                    for sat_index in range(4):
                                        start_idx = sat_index * 4

                                        # 4 fields for each satellite (ID, Elevation, Azimuth, SNR)
                                        for field_idx in range(4):
                                            data_idx = start_idx + field_idx
                                            if data_idx < len(satellite_data) and satellite_data[data_idx] and not satellite_data[data_idx].startswith('*'):
                                                processed_row.append(satellite_data[data_idx])
                                            else:
                                                processed_row.append('')  # Empty field

                                    # Append checksum at the end
                                    processed_row.append(checksum)

                                    # Adjust according to table column count
                                    target_columns = self.table.columnCount()
                                    if len(processed_row) < target_columns:
                                        processed_row.extend([''] * (target_columns - len(processed_row)))
                                    elif len(processed_row) > target_columns:
                                        processed_row = processed_row[:target_columns]
                                    
                                    self.processed_data.append(processed_row)
                                    
                            except (IndexError, ValueError) as e:
                                print(f"GSV row processing error: {e}")
                                continue
                
                return len(self.processed_data)
                
        except Exception as e:
            print(f"CSV reading error: {e}")
            return 0

    def process_nmea_file(self):
        """NMEA file processing function"""
        try:
            # Get selected parser
            selected_parser = self.parser_combo.currentData()

            # Create a temporary copy and save as data.txt
            temp_dir = tempfile.mkdtemp()
            temp_data_file = os.path.join(temp_dir, 'data.txt')
            shutil.copy2(self.selected_file, temp_data_file)

            # Find the selected parser script
            parser_script_path = os.path.join(os.path.dirname(self.selected_file), selected_parser)
            if not os.path.exists(parser_script_path):
                parser_script_path = os.path.join(os.path.dirname(__file__), selected_parser)
            
            if not os.path.exists(parser_script_path):
                QMessageBox.critical(
                    self, 
                    'Error', 
                    f'Parser file not found: {selected_parser}'
                )
                return
            
            # Copy the parser file
            temp_parser_file = os.path.join(temp_dir, selected_parser)
            shutil.copy2(parser_script_path, temp_parser_file)

            # Run the parser
            result = subprocess.run(
                ['python3', selected_parser], 
                cwd=temp_dir,
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            
            output_file_mapping = {
                'nmea_gga.py': 'nmea_gga_output.csv',
                'nmea_gsa.py': 'nmea_gsa_output.csv',
                'nmea_gll.py': 'nmea_gll_output.csv',
                'nmea_rmc.py': 'nmea_rmc_output.csv',
                'nmea_vtg.py': 'nmea_vtg_output.csv',
                'nmea_gsv.py': 'nmea_gsv_output.csv'
            }
            
            expected_output = output_file_mapping.get(selected_parser, 'output.csv')
            csv_output_path = os.path.join(temp_dir, expected_output)

            # Read the generated CSV file
            if os.path.exists(csv_output_path):
                valid_count = self.read_parser_csv_output(csv_output_path, selected_parser)

                # Update the table
                self.update_table()

                # Update status information
                parser_name = self.parser_combo.currentText()
                self.status_label.setText(f'Processed: {valid_count} valid sentences ({parser_name})')
                self.save_button.setEnabled(True)

                # Enable map button only for parsers containing coordinates
                if selected_parser in ['nmea_gga.py', 'nmea_gll.py', 'nmea_rmc.py']:
                    self.show_map_button.setEnabled(True)
                else:
                    self.show_map_button.setEnabled(False)

                if valid_count > 0:
                    QMessageBox.information(
                        self, 
                        'Success', 
                        f'{valid_count} valid sentences processed successfully!\n'
                        f'Data processed using {parser_name}.'
                    )
                else:
                    QMessageBox.warning(
                        self, 
                        'Warning', 
                        f'No valid sentences found! ({parser_name})'
                    )
            else:
                QMessageBox.warning(
                    self, 
                    'Warning', 
                    f'{selected_parser} was run but the CSV file could not be created!\n'
                    f'Script output: {result.stdout}\n'
                    f'Error: {result.stderr}'
                )

            # Clean up temporary files
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                'Error', 
                f'Error occurred while running parser: {str(e)}'
            )
    
    def update_table(self):
        """Update table function"""
        self.table.setRowCount(len(self.processed_data))
        
        for row, data in enumerate(self.processed_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

        # Adjust column widths
        self.table.resizeColumnsToContents()

        # Set minimum column widths
        for col in range(self.table.columnCount()):
            current_width = self.table.columnWidth(col)
            min_width = 100 if col == self.table.columnCount() - 1 else 150
            self.table.setColumnWidth(col, max(min_width, current_width))
    
    def load_default_map(self):
        """Load the default map"""
        try:
            # Create a world map
            m = folium.Map(location=[39.9334, 32.8597], zoom_start=6)  # Centered on Turkey

            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            m.save(temp_file.name)

            # Load the map into the web view
            self.map_view.load(QUrl.fromLocalFile(temp_file.name))
            
        except Exception as e:
            print(f"Error loading default map: {e}")

    def show_map(self):
        """Show GPS data on the map"""
        if not self.processed_data:
            QMessageBox.warning(self, 'Warning', 'No GPS data to display!')
            return
        
        try:
            # Determine coordinate columns based on selected parser type
            selected_parser = self.parser_combo.currentData()
            
            if selected_parser == "nmea_gga.py":
                # GGA parser: lat=1, lon=2
                lat_col, lon_col = 1, 2
            elif selected_parser == "nmea_gll.py":
                # GLL parser: lat=2, lon=3
                lat_col, lon_col = 2, 3
            elif selected_parser == "nmea_rmc.py":
                # RMC parser: lat=2, lon=3
                lat_col, lon_col = 2, 3
            else:
                QMessageBox.warning(self, 'Warning', 'No map support available for this parser type!')
                return

            # Extract coordinates
            coordinates = []
            for data in self.processed_data:
                try:
                    lat = float(data[lat_col])
                    lon = float(data[lon_col])
                    coordinates.append([lat, lon])
                except (ValueError, IndexError):
                    continue
            
            if not coordinates:
                QMessageBox.warning(self, 'Warning', 'No valid coordinate data found!')
                return

            # Calculate the average of the coordinates (for map center)
            avg_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
            avg_lon = sum(coord[1] for coord in coordinates) / len(coordinates)

            # Create a map
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15)
            
            # If there is more than one point, draw a route
            if len(coordinates) > 1:
                folium.PolyLine(
                    coordinates,
                    color='blue',
                    weight=3,
                    opacity=1.0,
                    popup='GPS Route'
                ).add_to(m)

            # Add a marker for each GPS point
            for i, coord in enumerate(coordinates):
                lat, lon = coord
                folium.CircleMarker(
                    [lat, lon],
                    radius=8,
                    color='lightblue',
                    fill=True,
                    fill_color='lightblue',
                    fill_opacity=1.0,
                    popup=f'Point {i+1}<br>Latitude: {lat}<br>Longitude: {lon}',
                    tooltip=f'Point {i+1}'
                ).add_to(m)

            # Create a temporary file and save
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
            m.save(temp_file.name)

            # Load the map into the web view
            self.map_view.load(QUrl.fromLocalFile(temp_file.name))
            
            QMessageBox.information(
                self,
                'Success',
                f'{len(coordinates)} GPS points displayed on the map!'
            )
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Map creation error: {str(e)}')
    
    def save_csv(self):
        """CSV file saving function"""
        if not self.processed_data:
            QMessageBox.warning(self, 'Warning', 'No data to save!')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save CSV File',
            'nmea_output.csv', 
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    # Write table headers
                    headers = []
                    for col in range(self.table.columnCount()):
                        headers.append(self.table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)

                    # Write the data
                    writer.writerows(self.processed_data)
                
                QMessageBox.information(
                    self,
                    'Success',
                    f'Data successfully saved:\n{file_path}'
                )
                self.status_label.setText(f'CSV saved: {os.path.basename(file_path)}')

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'File saving error: {str(e)}')

    def clear_data(self):
        """Data clearing function"""
        self.table.setRowCount(0)
        self.processed_data = []
        self.selected_file = None
        self.file_label.setText('No file selected')
        self.process_button.setEnabled(False)
        self.parser_combo.setEnabled(False)  # Disable parser selection
        self.save_button.setEnabled(False)
        self.show_map_button.setEnabled(False)  # Disable map button
        self.status_label.setText('Cleared - Please select an NMEA file')

        # Reset table headers to default
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(self.default_headers)

        # Reload default map
        self.load_default_map()

def main():
    """Main function"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create and show main window
    window = NMEAParserGUI()
    window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()