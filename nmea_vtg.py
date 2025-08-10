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
    "VTG Sentence",        # Index 0: GPVTG
    "True Track",          # Index 1: True track angle
    "True Track Direction Indicator", # Index 2: True track direction indicator
    "Magnetic Track",     # Index 3: Magnetic track angle
    "Magnetic Track Direction Indicator", # Index 4: Magnetic track direction indicator
    "Speed in Knots",      # Index 5: Speed over ground in knots
    "Knot Units",        # Index 6: Knot units (N for nautical miles)
    "Speed in Kilometers",  # Index 7: Speed over ground in kilometers per hour
    "Kilometer Units",     # Index 8: Kilometer units (K for kilometers)
    "Checksum"              # Index 9: Checksum
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
    if not split_sentence[0].endswith("VTG"):
        print("This is not a VTG sentence, skipping.")
        return None
    
    true_track = split_sentence[1]  # True track angle in degrees
    true_track_indicator = split_sentence[2]  # True track direction indicator
    magnetic_track = split_sentence[3]  # Magnetic track angle in degrees
    magnetic_track_indicator = split_sentence[4]  # Magnetic track direction indicator
    speed_knots = split_sentence[5]  # Speed over ground in knots
    speed_knots_units = split_sentence[6]  # Knot units (N for nautical miles)
    speed_kilometers = split_sentence[7]  # Speed over ground in kilometers per hour
    speed_kilometers_units = split_sentence[8]  # Kilometer units (K for kilometers)

    split_sentence.append(checksum)  # Append checksum to the end of the split sentence

    print("VTG Sentence Components:")
    for i in range(len(split_sentence)):
        component_name = components[i] if i < len(components) else f"Field {i}"
        print(f" {component_name}: {split_sentence[i]}")

    return [true_track, magnetic_track, speed_knots, speed_kilometers, checksum]

nmea_sentences = read_nmea_data("nmea_data_vtg.txt")

all_data = []
vtg_sentence_count = 0

for sentence in nmea_sentences:
    try:
        if sentence.startswith('$') and sentence[1:].split(',')[0].endswith("VTG"):
            vtg_sentence_count += 1
            print(f"\n--- NMEA VTG Sentence {vtg_sentence_count} ---")

        data = nmea_sentence(sentence)
        if data:
            all_data.append(data)
    except ValueError as e:
        print(f"Error processing sentence: {e}")

if all_data:
    csv_file = "nmea_vtg_output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["true_track", "magnetic_track", "speed_knots", "speed_kilometers", "checksum"])
        writer.writerows(all_data)
    print(f"\n{len(all_data)} rows of VTG data saved to '{csv_file}'.")
else:
    print("No valid VTG data found to save.")
