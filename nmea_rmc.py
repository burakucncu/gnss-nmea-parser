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
    "NMEA Sentence",        # Index 0: GPRMC
    "UTC Time",            # Index 1: UTC time
    "Status",              # Index 2: A=active, V=void
    "Latitude",            # Index 3: Latitude
    "N/S Indicator",       # Index 4: N=north, S=south
    "Longitude",           # Index 5: Longitude
    "E/W Indicator",       # Index 6: E=east, W=west
    "Speed",               # Index 7: Speed over ground
    "Direction",           # Index 8: Direction over ground
    "Date",                # Index 9: Date
    "Magnetic Variation",  # Index 10: Magnetic variation
    "Variation Direction", # Index 11: E=east, W=west
    "Checksum"             # Index 12: Checksum
]

def nmea_sentence(sentence):
    if not sentence.startswith('$'):
        raise ValueError('NMEA sentence must start with "$"')
    sentence = sentence[1:]  # Remove the leading '$'
    
    if '*' in sentence:
        sentence_part, checksum = sentence.split('*')
        checksum = f"*{checksum}"
    else:
        sentence_part = sentence
        checksum = ""
    
    split_sentence = sentence_part.split(',')
    if not split_sentence[0].endswith("RMC"):
        print("This is not a RMC sentence, skipping.")
        return None
    
    utc_time = split_sentence[1]  # UTC time
    status = split_sentence[2]  # A=active, V=void
    latitude = split_sentence[3]
    lat_direction = split_sentence[4]  # N=north, S=south
    longitude = split_sentence[5]
    lon_direction = split_sentence[6]  # E=east, W=west
    speed = split_sentence[7]  # Speed over ground in knots
    direction = split_sentence[8]  # Direction over ground in degrees
    date = split_sentence[9]  # Date in DDMMYY format
    magnetic_variation = split_sentence[10] if len(split_sentence) > 10 else ""  # Magnetic variation in degrees
    variation_direction = split_sentence[11] if len(split_sentence) > 11 else ""  # E=east, W=west

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

    lat_degrees_formatted = f"{lat_degrees:.6f}"
    lon_degrees_formatted = f"{lon_degrees:.6f}"
    
    split_sentence[3] = lat_degrees_formatted
    split_sentence[5] = lon_degrees_formatted

    if '.' in utc_time:
        time_parts = utc_time.split('.')
        time_base = time_parts[0]
        milliseconds = time_parts[1]
        if len(time_base) >= 6:
            utc_time_formatted = f"{time_base[:2]}:{time_base[2:4]}:{time_base[4:]}.{milliseconds}"
        else:
            utc_time_formatted = utc_time
    else:
        utc_time_formatted = f"{utc_time[:2]}:{utc_time[2:4]}:{utc_time[4:]}" if len(utc_time) >= 6 else utc_time

    split_sentence[1] = utc_time_formatted

    split_sentence.append(checksum)

    print("RMC Sentence Components:")
    for i in range(len(split_sentence)):
        if i < len(components):
            print(f" {components[i]}: {split_sentence[i]}")
        else:
            print(f" Index {i}: {split_sentence[i]}")

    return [utc_time_formatted, status, lat_degrees_formatted, lon_degrees_formatted, speed, direction, date, magnetic_variation, variation_direction, checksum]

nmea_sentences = read_nmea_data("data.txt")

all_data = []
rmc_sentence_count = 0

for sentence in nmea_sentences:
    try:
        if sentence.startswith('$') and sentence[1:].split(',')[0].endswith("RMC"):
            rmc_sentence_count += 1
            print(f"\n--- NMEA RMC Sentence {rmc_sentence_count} ---")

        data = nmea_sentence(sentence)
        if data:
            all_data.append(data)
    except ValueError as e:
        print(f"Error processing sentence: {e}")

# CSV'ye kaydet
if all_data:
    csv_file = "nmea_rmc_output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["utc_time", "status", "latitude", "longitude", "speed", "direction", "date", "magnetic_variation", "variation_direction", "checksum"])
        writer.writerows(all_data)
    print(f"\n{len(all_data)} rows of RMC data saved to '{csv_file}'.")
else:
    print("No valid RMC data found to save.")

