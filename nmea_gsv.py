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
    if not split_sentence[0].endswith("GSV"):
        print("This is not a GSV sentence, skipping.")
        return None
    
    # GSV sentence'ın temel componentleri
    base_components = [
        "NMEA Sentence",           # Index 0: GPGSV
        "Total GSV Sentences",     # Index 1: Total number of GSV sentences
        "Sentence Number",         # Index 2: Current sentence number
        "Satellites in View"       # Index 3: Total satellites in view
    ]
    
    # Dinamik olarak uydu bilgileri için componentleri oluştur
    # Her GSV sentence'ında en fazla 4 uydu bilgisi olabilir
    # Index 4'ten başlayarak her 4 field bir uydu bilgisini temsil eder
    satellite_components = []
    
    # Uydu sayısını hesapla (checksum hariç, ilk 4 field hariç)
    available_fields = len(split_sentence) - 4  # İlk 4 field: sentence, total, number, sat_count
    satellite_count = available_fields // 4  # Her uydu 4 field kullanır
    
    for i in range(satellite_count):
        satellite_num = i + 1
        satellite_components.extend([
            f"Satellite {satellite_num} ID",
            f"Satellite {satellite_num} Elevation",
            f"Satellite {satellite_num} Azimuth", 
            f"Satellite {satellite_num} SNR"
        ])
    
    # Son kalan fieldlar (4'ün katı olmayan) için
    remaining_fields = available_fields % 4
    if remaining_fields > 0:
        satellite_num = satellite_count + 1
        field_names = ["ID", "Elevation", "Azimuth", "SNR"]
        for i in range(remaining_fields):
            satellite_components.append(f"Satellite {satellite_num} {field_names[i]}")
    
    # Tüm componentleri birleştir
    components = base_components + satellite_components + ["Checksum"]
    
    # Checksum'ı split_sentence'ın sonuna ekle
    split_sentence.append(checksum)

    print("GSV Sentence Components:")
    for i in range(len(split_sentence)):
        if i < len(components):
            print(f" {components[i]}: {split_sentence[i]}")
        else:
            print(f" Index {i}: {split_sentence[i]}")
    
    # Return için tüm verileri topla
    return split_sentence

# Read NMEA data from txt file
nmea_sentences = read_nmea_data("nmea_data_gsv.txt")

all_data = []
gsv_sentence_count = 0

for sentence in nmea_sentences:
    try:
        if sentence.startswith('$') and sentence[1:].split(',')[0].endswith("GSV"):
            gsv_sentence_count += 1
            print(f"\n--- NMEA GSV Sentence {gsv_sentence_count} ---")

        data = nmea_sentence(sentence)
        if data:
            all_data.append(data)
    except ValueError as e:
        print(f"Error processing sentence: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# CSV'ye kaydet
if all_data:
    csv_file = "nmea_gsv_output.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Header oluştur - en uzun satırın field sayısını bul
        max_fields = max(len(row) for row in all_data) if all_data else 0
        header = []
        header.extend(["NMEA_Sentence", "Total_GSV_Sentences", "Sentence_Number", "Satellites_in_View"])
        
        # Dinamik uydu field'larını ekle
        satellite_count = (max_fields - 5) // 4  # 4 temel field + checksum = 5
        for i in range(satellite_count):
            sat_num = i + 1
            header.extend([f"Sat_{sat_num}_ID", f"Sat_{sat_num}_Elevation", f"Sat_{sat_num}_Azimuth", f"Sat_{sat_num}_SNR"])
        
        # Kalan field'lar için
        remaining = (max_fields - 5) % 4
        if remaining > 0:
            sat_num = satellite_count + 1
            field_names = ["ID", "Elevation", "Azimuth", "SNR"]
            for i in range(remaining):
                header.append(f"Sat_{sat_num}_{field_names[i]}")
        
        header.append("Checksum")
        
        writer.writerow(header)
        writer.writerows(all_data)
    print(f"\n{len(all_data)} rows of GSV data saved to '{csv_file}'.")
else:
    print("No valid GSV data found to save.")