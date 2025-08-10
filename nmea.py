import csv


def read_nmea_data(filename):
    """Reads NMEA data from txt file and returns as list"""
    sentences = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()  
                if line: 
                    sentences.append(line)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    return sentences

components = [
    "NMEA Sentence",
    "Time of fix (UTC)",
    "Latitude",
    "N/S Indicator",
    "Longitude",
    "E/W Indicator",
    "Fix quality",
    "Number of satellites in view",
    "Horizontal dilution of position HDOP",
    "Altitude",
    "Altitude units",
    "Geoidal separation",
    "Geoidal separation units",
    "Age of differential GPS data (if applicable)",
    "Checksum (optional)"
]
def nmea_sentence(sentence):

    if not sentence.startswith('$'):
        raise ValueError("NMEA sentence must start with '$'")
    sentence = sentence[1:]  
    split_sentence = sentence.split(',')

    if not split_sentence[0].endswith("GGA"):
        print("This is not a GGA sentence, skipping.")
        return None

    utc_time = split_sentence[1]
    latitude = split_sentence[2]
    lat_direction = split_sentence[3]
    longitude = split_sentence[4]
    lon_direction = split_sentence[5]
    altitude = split_sentence[9]
    satellites = split_sentence[7]
    fix_quality = split_sentence[6]

    lat_degrees = float(latitude[:2]) + float(latitude[2:]) / 60
    lon_degrees = float(longitude[:3]) + float(longitude[3:]) / 60

    if lat_direction == 'S':
        lat_degrees = -lat_degrees
    else:
        lat_degrees = lat_degrees

    if lon_direction == 'W':
        lon_degrees = -lon_degrees
    else:
        lon_degrees = lon_degrees

    # Yuvarlanmış değerleri hem ekran hem CSV için kullan
    lat_degrees_formatted = f"{lat_degrees:.6f}"
    lon_degrees_formatted = f"{lon_degrees:.6f}"
    
    split_sentence[2] = lat_degrees_formatted
    split_sentence[4] = lon_degrees_formatted

    # UTC zamanını formatla (örnek: 170141.751 -> 17:01:41.751)
    if '.' in utc_time:
        # Nokta varsa, saat:dakika:saniye.milisaniye formatına çevir
        time_parts = utc_time.split('.')
        time_base = time_parts[0]  # 170141
        milliseconds = time_parts[1]  # 751
        if len(time_base) >= 6:
            utc_time_formatted = f"{time_base[:2]}:{time_base[2:4]}:{time_base[4:]}.{milliseconds}"
        else:
            utc_time_formatted = utc_time
    else:
        # Nokta yoksa, standart formatla (6 karakter)
        utc_time_formatted = f"{utc_time[:2]}:{utc_time[2:4]}:{utc_time[4:]}" if len(utc_time) >= 6 else utc_time

    split_sentence[1] = utc_time_formatted

    print("GGA Sentence Components:")
    for i in range(len(split_sentence)):
        print(f" {components[i]}: {split_sentence[i]}")

    # utc_time_formatted, lat, lon, altitude, satellites, fix_quality values
    return [utc_time_formatted, lat_degrees_formatted, lon_degrees_formatted, altitude, satellites, fix_quality]

# Read NMEA data from txt file
nmea_sentences = read_nmea_data("data.txt")

# List to collect all data
all_data = []

# Process each NMEA sentence
for i, sentence in enumerate(nmea_sentences):
    print(f"\n--- NMEA GGA Sentence {i+1} ---")
    result = nmea_sentence(sentence)
    if result:  # If valid result returned, add to list
        all_data.append(result)


if all_data:
    csv_file = "nmea_output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["utc_time_formatted", "latitude", "longitude", "altitude",  "satellites", "fix_quality"])
        writer.writerows(all_data)
    print(f"\n{len(all_data)} rows of data saved to '{csv_file}'.")
else:
    print("No valid data found to save.")



