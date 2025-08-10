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
    "NMEA Sentence",  # Index 0: GPGSA
    "Mode 1",        # Index 1: A=automatic, M=manual  
    "Mode 2",        # Index 2: 1=no fix, 2=2D, 3=3D
    "Sat ID 1",      # Index 3-14: Satellite IDs
    "Sat ID 2", 
    "Sat ID 3",
    "Sat ID 4",
    "Sat ID 5",
    "Sat ID 6", 
    "Sat ID 7",
    "Sat ID 8",
    "Sat ID 9",
    "Sat ID 10",
    "Sat ID 11",
    "Sat ID 12",
    "PDOP",          # Index 15: Position Dilution of Precision
    "HDOP",          # Index 16: Horizontal Dilution of Precision
    "VDOP",          # Index 17: Vertical Dilution of Precision
    "Checksum"      # Index 18: Checksum (optional)
]

def nmea_sentence(sentence):
    if not sentence.startswith('$'):
        raise ValueError("NMEA sentence must start with '$'")
    sentence = sentence[1:]  

    if '*' in sentence:
        sentence_part, checksum = sentence.split('*')
        checksum = f"*{checksum}"
    else:
        sentence_part = sentence
        checksum = ""

    split_sentence = sentence_part.split(',')
    if not split_sentence[0].endswith("GSA"):
        return None

    mode_1 = split_sentence[1]  # A = automatic, M = manual
    mode_2 = split_sentence[2]  # 1 = no fix, 2 = 2D fix, 3 = 3D fix
    satellite_ids = [sat for sat in split_sentence[3:15] if sat]  # Remove empty satellite IDs
    pdop = split_sentence[15]
    hdop = split_sentence[16]
    vdop = split_sentence[17].split('*')[0]  # Remove checksum if present

    split_sentence.append(checksum)

    print("GSA Sentence Components:")
    for i in range(len(split_sentence)):
        component_name = components[i] if i < len(components) else f"Field {i}"
        print(f" {component_name}: {split_sentence[i]}")

    return {
        "Mode 1": mode_1,
        "Mode 2": mode_2,
        "Satellite IDs": satellite_ids,
        "PDOP": pdop,
        "HDOP": hdop,
        "VDOP": vdop
    }

nmea_sentences = read_nmea_data("nmea_data_gsa.txt")

all_data = []
gsa_sentence_count = 0

for sentence in nmea_sentences:
    try:
        if sentence.startswith('$') and sentence[1:].split(',')[0].endswith("GSA"):
            gsa_sentence_count += 1
            print(f"\n--- NMEA GSA Sentence {gsa_sentence_count} ---")
        
        data = nmea_sentence(sentence)
        if data:
            all_data.append(data)
    except ValueError as e:
        print(f"Error processing sentence: {e}")

if all_data:
    csv_file = "nmea_gsa_data.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Mode 1", "Mode 2", "Satellite IDs", "PDOP", "HDOP", "VDOP"])
        
        for data in all_data:
            # Dictionary'den değerleri çıkar ve CSV formatına dönüştür
            satellite_ids_str = ','.join(data["Satellite IDs"])  # Liste olarak birleştir
            row = [
                data["Mode 1"],
                data["Mode 2"], 
                satellite_ids_str,
                data["PDOP"],
                data["HDOP"],
                data["VDOP"]
            ]
            writer.writerow(row)
            
    print(f"\nProcessed {gsa_sentence_count} GSA sentences. Data saved to '{csv_file}'.")
else:
    print("No valid GSA sentences found.")