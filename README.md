# GNSS NMEA Parser

## Overview
This project is a Python-based NMEA (National Marine Electronics Association) sentence parser specifically designed to process GPS data from NMEA 0183 format. The parser extracts essential GPS information including latitude, longitude, and altitude from GGA (Global Positioning System Fix Data) sentences and exports the processed data to a CSV file for further analysis.

## Features
- **NMEA File Reading**: Reads NMEA sentences from text files
- **GGA Sentence Parsing**: Specifically processes GGA sentences containing GPS fix data
- **Coordinate Conversion**: Converts NMEA coordinate format (DDMM.MMMM) to decimal degrees
- **Hemisphere Detection**: Handles North/South and East/West indicators for accurate positioning
- **CSV Export**: Exports processed GPS data to CSV format for easy analysis
- **Error Handling**: Includes file not found and invalid sentence format handling
- **Detailed Output**: Displays all NMEA sentence components for debugging and verification
- **Graphical User Interface**: User-friendly PyQt5-based GUI for easy file processing and visualization
- **Interactive Maps**: Real-time map visualization using Folium with GPS points and route tracking
- **Data Table View**: Tabular display of processed GPS coordinates and altitude data

## File Structure
```
nmea.py         - Main Python script containing the NMEA parser
gui.py          - PyQt5-based graphical user interface for NMEA processing
data.txt        - Input file containing NMEA sentences
nmea_output.csv - Output CSV file with processed GPS data
README.md       - This documentation file
qgis_files/     - QGIS project files for advanced spatial analysis
```

## How It Works

### Input Data Format
The parser expects NMEA GGA sentences in the following format:
```
$GPGGA,HHMMSS,DDMM.MMMM,N/S,DDDMM.MMMM,E/W,Q,NN,H.H,A.A,M,G.G,M,T,CCCC*hh
```

**Where:**
- `HHMMSS`: Time of fix (UTC)
- `DDMM.MMMM`: Latitude in degrees and minutes
- `N/S`: North or South hemisphere
- `DDDMM.MMMM`: Longitude in degrees and minutes
- `E/W`: East or West hemisphere
- `Q`: Fix quality indicator
- `NN`: Number of satellites in view
- `H.H`: Horizontal dilution of position (HDOP)
- `A.A`: Altitude above mean sea level
- `M`: Altitude units (meters)
- `G.G`: Geoidal separation
- `M`: Geoidal separation units
- `T`: Age of differential GPS data
- `CCCC`: Checksum

### Processing Steps
1. **File Reading**: The script reads NMEA sentences from `data.txt`
2. **Validation**: Checks if sentences start with '$' and are GGA format
3. **Parsing**: Splits the sentence into components
4. **Coordinate Conversion**: 
   - Converts latitude from DDMM.MMMM to decimal degrees
   - Converts longitude from DDDMM.MMMM to decimal degrees
   - Applies hemisphere corrections (negative for South/West)
5. **Data Collection**: Stores latitude, longitude, and altitude for each valid sentence
6. **CSV Export**: Writes all processed data to `nmea_output.csv`

### Output Format
The CSV file contains three columns:
- **latitude**: Decimal degrees (negative for Southern hemisphere)
- **longitude**: Decimal degrees (negative for Western hemisphere)  
- **altitude**: Height above sea level in meters

## Usage

### Prerequisites
- Python 3.x
- For command-line usage: No additional libraries required (uses built-in `csv` module)
- For GUI usage: PyQt5, folium libraries required

### Installation
For GUI usage, install the required dependencies:
```bash
pip install PyQt5 folium
```

### Running the Command-Line Parser
1. Place your NMEA data in `data.txt`
2. Run the script:
   ```bash
   python3 nmea.py
   ```
3. Check the output in `nmea_output.csv`

### Running the GUI Application
1. Launch the graphical interface:
   ```bash
   python3 gui.py
   ```
2. Use the GUI features:
   - **File Selection**: Click "NMEA Dosyası Seç" to select NMEA or CSV files
   - **Data Processing**: Click "Verileri İşle" to parse the selected file
   - **Table View**: View processed GPS data in the left panel table
   - **Map Visualization**: Click "Haritada Göster" to display GPS points on an interactive map
   - **Save Results**: Click "CSV Olarak Kaydet" to export processed data
   - **Clear Data**: Click "Temizle" to reset the application

### Sample Input
```
$GPGGA,120000,4051.234,N,02923.456,E,1,07,1.0,45.5,M,34.0,M,,*5A
$GPGGA,120005,4051.300,N,02923.500,E,1,08,0.9,46.0,M,34.1,M,,*60
```

### Sample Output
```csv
latitude,longitude,altitude
40.8539,29.390933333333333,45.5
40.855,29.391666666666666,46.0
```

## GUI Application Features

### Interface Overview
The NMEA Parser GUI provides an intuitive graphical interface built with PyQt5 for processing and visualizing GPS data. The application features a dual-panel layout with data table view on the left and interactive map visualization on the right.

### Key GUI Features

#### 🗂️ **File Management**
- **Multi-format Support**: Supports NMEA (.nmea, .txt) and CSV files
- **Drag & Drop Interface**: Easy file selection through file dialog
- **File Validation**: Automatic detection and processing of different file formats

#### 📊 **Data Processing & Display**
- **Real-time Table View**: Displays processed GPS coordinates (latitude, longitude, altitude)
- **Data Validation**: Automatic filtering of invalid or corrupted GPS data
- **Progress Feedback**: Status updates and processing information
- **Error Handling**: User-friendly error messages and warnings

#### 🗺️ **Interactive Map Visualization**
- **Live Map Display**: Real-time GPS point visualization using Folium
- **Route Tracking**: Automatic connection of GPS points to show travel routes
- **Interactive Markers**: Clickable markers with detailed coordinate information
- **Zoom Controls**: Full pan and zoom capabilities for detailed examination
- **Multi-point Support**: Handles single points to complex route data

#### 💾 **Export Capabilities**
- **CSV Export**: Save processed data in standard CSV format
- **Custom File Names**: User-defined output file naming
- **Data Preservation**: Maintains coordinate precision and altitude information

#### 🎛️ **User Controls**
- **Process Button**: Initiates NMEA data parsing and conversion
- **Map Button**: Generates and displays interactive map visualization
- **Save Button**: Exports processed data to CSV format
- **Clear Button**: Resets application and clears all data

### GUI Workflow
1. **Launch Application**: Start the GUI with `python3 gui.py`
2. **Select File**: Choose NMEA or CSV file using the file browser
3. **Process Data**: Click "Process Data" to parse GPS coordinates
4. **View Results**: Review data in the table and map panels
5. **Export Data**: Save results as CSV for further analysis
6. **Reset**: Clear all data to start a new session

### Technical Implementation
- **Framework**: PyQt5 for cross-platform GUI development
- **Web Engine**: QtWebEngine for embedded map display
- **Mapping**: Folium library for interactive map generation
- **Data Processing**: Integration with existing NMEA parser functionality

## Visualizing Data in QGIS

The generated CSV file can be easily imported into QGIS for visualization and spatial analysis:

### Steps to Open CSV in QGIS:
1. **Open QGIS** and create a new project
2. **Add Layer**: Go to `Layer` → `Add Layer` → `Add Delimited Text Layer...`
3. **Select File**: Browse and select your `nmea_output.csv` file
4. **Configure Import Settings**:
   - **File Format**: CSV (comma separated values)
   - **Geometry Definition**: Point coordinates
   - **X field**: Select `longitude`
   - **Y field**: Select `latitude`
   - **Geometry CRS**: Choose `EPSG:4326 - WGS 84`
5. **Click OK** to import the data
6. **Styling** (Optional):
   - Right-click on the layer → Properties → Symbology
   - Customize point symbols, colors, and size
   - Use altitude values for graduated symbols or color ramps

### QGIS Features for GPS Data:
- 📊 **Attribute Table**: View all coordinate and altitude data
- 🗺️ **Background Maps**: Add OpenStreetMap or satellite imagery
- 📏 **Measurements**: Calculate distances and areas
- 📈 **Elevation Profiles**: Create altitude vs distance charts
- 🎯 **Spatial Analysis**: Buffer zones, proximity analysis
- 📤 **Export Options**: Save as KML, Shapefile, or other formats

## Code Structure

### Command-Line Parser Functions
- **`read_nmea_data(filename)`**: Reads NMEA sentences from file
- **`nmea_sentence(sentence)`**: Parses individual NMEA sentences and extracts GPS data

### GUI Application Classes
- **`NMEAParserGUI`**: Main application class handling GUI interface and user interactions
  - **`initUI()`**: Initializes the user interface layout and components
  - **`select_file()`**: Handles file selection through dialog box
  - **`process_data()`**: Processes NMEA or CSV files and extracts GPS data
  - **`process_nmea_file()`**: Specifically handles NMEA format files
  - **`process_csv_file()`**: Handles pre-processed CSV files
  - **`update_table()`**: Updates the data table with processed GPS coordinates
  - **`show_map()`**: Generates and displays interactive map with GPS points
  - **`save_csv()`**: Exports processed data to CSV format
  - **`clear_data()`**: Resets application state and clears all data
  - **`load_default_map()`**: Loads initial map view centered on Turkey

### Main Process
1. Read all NMEA sentences from input file
2. Process each sentence individually
3. Collect valid GPS data points
4. Export all data to CSV file

## Error Handling
- **File Not Found**: Gracefully handles missing input files
- **Invalid Format**: Skips non-GGA sentences with appropriate messages
- **Malformed Data**: Validates sentence structure before processing

## Applications
This parser can be used for:
- 📍 GPS data analysis and visualization
- 🗺️ Route tracking and mapping
- 🧭 Navigation system development
- 🌍 Geographic information system (GIS) applications
- 🔬 Research in positioning and navigation
- 🚗 Vehicle tracking and fleet management
- 🎯 Field data collection and survey applications
- 📱 Mobile application GPS data processing
- 🛰️ GNSS data validation and quality assessment

## Future Enhancements
- [ ] Support for other NMEA sentence types (RMC, VTG, etc.)
- [ ] Real-time data processing capabilities
- [ ] Advanced filtering and data validation
- [ ] Integration with mapping libraries
- [ ] Support for different coordinate systems
- [ ] GPS track analysis and statistics
- [ ] Export to KML and GPX formats
- [ ] Multi-language support for GUI
- [ ] Dark theme option for GUI
- [ ] Elevation profile visualization
- [ ] Speed and heading calculations from GPS data

## License
This project is open source and available under the [MIT License](LICENSE).

---

> **Note**: This project was developed for learning purposes to enhance my knowledge and skills in the GNSS (Global Navigation Satellite System) field and GPS data processing.
