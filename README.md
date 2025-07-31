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

## File Structure
```
nmea.py         - Main Python script containing the NMEA parser
data.txt        - Input file containing NMEA sentences
nmea_output.csv - Output CSV file with processed GPS data
README.md       - This documentation file
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
- No additional libraries required (uses built-in `csv` module)

### Running the Parser
1. Place your NMEA data in `data.txt`
2. Run the script:
   ```bash
   python3 nmea.py
   ```
3. Check the output in `nmea_output.csv`

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

### Functions
- **`read_nmea_data(filename)`**: Reads NMEA sentences from file
- **`nmea_sentence(sentence)`**: Parses individual NMEA sentences and extracts GPS data

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

## Future Enhancements
- [ ] Support for other NMEA sentence types (RMC, VTG, etc.)
- [ ] Real-time data processing capabilities
- [ ] Advanced filtering and data validation
- [ ] Integration with mapping libraries
- [ ] Support for different coordinate systems

## License
This project is open source and available under the [MIT License](LICENSE).

---

> **Note**: This project was developed for learning purposes to enhance my knowledge and skills in the GNSS (Global Navigation Satellite System) field and GPS data processing.
