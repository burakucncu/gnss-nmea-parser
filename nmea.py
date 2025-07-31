import csv


def read_nmea_data(filename):
    """Txt dosyasından NMEA verilerini okur ve liste olarak döndürür"""
    sentences = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  
                if line: 
                    sentences.append(line)
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {filename}")
        return []
    return sentences

components = [
    "GGA Sentence",
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
        print("Bu GGA cümlesi değil, atlanıyor.")
        return None

    latitude = split_sentence[2]
    lat_direction = split_sentence[3]
    longitude = split_sentence[4]
    lon_direction = split_sentence[5]
    altitude = split_sentence[9]

    lat_degrees = float(latitude[:2]) + float(latitude[2:]) / 60
    lon_degrees = float(longitude[:3]) + float(longitude[3:]) / 60
    if lat_direction == 'S':
        lat_degrees = -lat_degrees
    if lon_direction == 'W':
        lon_degrees = -lon_degrees

    split_sentence[2] = lat_degrees
    split_sentence[4] = lon_degrees

    print("NMEA Sentence Components:")
    for i in range(len(split_sentence)):
        print(f" {components[i]}: {split_sentence[i]}")
    
    # Sadece lat, lon, altitude değerlerini döndür
    return [lat_degrees, lon_degrees, altitude]

# Txt dosyasından NMEA verilerini oku
nmea_sentences = read_nmea_data("data.txt")

# Tüm verileri toplamak için liste
all_data = []

# Her NMEA cümlesini işle
for i, sentence in enumerate(nmea_sentences):
    print(f"\n--- NMEA Cümlesi {i+1} ---")
    result = nmea_sentence(sentence)
    if result:  # Eğer geçerli bir sonuç döndüyse listeye ekle
        all_data.append(result)

# Tüm verileri CSV dosyasına yaz
if all_data:
    csv_file = "nmea_output.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["latitude", "longitude", "altitude"])
        writer.writerows(all_data)
    print(f"\n{len(all_data)} satır veri '{csv_file}' dosyasına kaydedildi.")



