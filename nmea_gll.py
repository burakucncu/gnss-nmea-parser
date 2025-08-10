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
    "GLL Sentence",  # Index 0: GPGLL
    "Latitude",      # Index 1: Latitude in degrees and minutes
    "N/S Indicator", # Index 2: N=north, S=south
    "Longitude",     # Index 3: Longitude in degrees and minutes
    "E/W Indicator", # Index 4: E=east, W=west
    "UTC Time",      # Index 5: UTC time of position fix
    "Status",        # Index 6: A=active, V=void
    "Checksum"       # Index 7: Checksum
]

def nmea_sentence(sentence):
    if not sentence.startswith('$'):
        raise ValueError("NMEA sentence must start with '$'")
    sentence = sentence[1:]  # Remove the leading '$'

    if '*' in sentence:
        sentence_part, checksum = sentence.split('*')
        checksum = f"*{checksum}"
    else:
        sentence_part = sentence
        checksum = ""

    split_sentence = sentence_part.split(',')
    if not split_sentence[0].endswith("GLL"):
        print("This is not a GLL sentence, skipping.")
        return None
    
    latitude = split_sentence[1]  # Latitude in degrees and minutes
    lat_direction = split_sentence[2]  # N=north, S=south
    longitude = split_sentence[3]  # Longitude in degrees and minutes
    lon_direction = split_sentence[4]  # E=east, W=west
    utc_time = split_sentence[5]  # UTC time of position fix
    status = split_sentence[6]  # A=active, V=void

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

    split_sentence[1] = lat_degrees_formatted
    split_sentence[3] = lon_degrees_formatted

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

    split_sentence[5] = utc_time_formatted

    split_sentence.append(checksum)

    print("GLL Sentence Components:")
    for i in range(len(split_sentence)):
        if i < len(components):
            print(f" {components[i]}: {split_sentence[i]}")
        else:
            print(f" Index {i}: {split_sentence[i]}")

    return [utc_time_formatted, status, lat_degrees_formatted, lon_degrees_formatted, checksum]

nmea_sentences = read_nmea_data("data.txt")

all_data = []
gll_sentence_count = 0

for sentence in nmea_sentences:
    try:
        if sentence.startswith('$') and sentence[1:].split(',')[0].endswith("GLL"):
            gll_sentence_count += 1
            print(f"\n--- NMEA GLL Sentence {gll_sentence_count} ---")

        data = nmea_sentence(sentence)
        if data:
            all_data.append(data)
    except ValueError as e:
        print(f"Error processing sentence: {e}")

if all_data:
    csv_file = "nmea_gll_output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["UTC Time", "Status", "Latitude", "Longitude", "Checksum"])
        writer.writerows(all_data)
    print(f"\n{len(all_data)} rows of GLL data saved to '{csv_file}'.")
else:
    print("No valid GLL data found to save.")


