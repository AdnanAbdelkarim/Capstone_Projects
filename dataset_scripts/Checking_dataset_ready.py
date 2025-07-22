import os

# ✅ Path to your dataset labels folder
LABELS_DIR = r'C:\Users\student\Desktop\EV_MODEL\dataset\train\labels'

# ✅ List of vehicle models (from data.yaml order)
vehicle_models = ['Tesla Model 3', 'Kia EV3 Long Range', 'BYD ATTO 3', 'Mercedes-Benz CLA 250+', 'MG MG4 Electric 64 kWh', 'BMW iX xDrive40', 'BMW i3 120 Ah', 'Skoda Elroq 85', 'Renault 5 E-Tech 52kWh 150hp', 'BYD HAN', 'BYD DOLPHIN 60.4 kWh', 'Mercedes-Benz EQS 450+', 'Audi e-tron 55 quattro', 'BMW i4 eDrive40', 'BYD SEAL 82.5 kWh AWD Excellence', 'Volkswagen ID.4 Pro', 'KGM Torres EVX', 'Hyundai Kona Electric 65 kWh', 'Hyundai IONIQ 5 84 kWh RWD', 'Volkswagen e-Golf', 'Fiat 500e Hatchback 42 kWh', 'Kia Niro EV', 'BMW iX1 xDrive30', 'Toyota bZ4X FWD', 'Renault Scenic E-Tech EV87 220hp', 'CUPRA Born 150 kW - 58 kWh', 'BYD SEALION 7 91.3 kWh AWD Excellence', 'Mazda 6e', 'Volvo EX30 Single Motor ER', 'Mercedes-Benz EQC 400 4MATIC', 'Nissan Leaf', 'Hyundai INSTER Long Range', 'Kia EV6 Long Range 2WD', 'Mercedes-Benz EQB 250+', 'Mini Countryman E', 'Renault Megane E-Tech EV60 220hp', 'Kia EV4 Hatchback Long Range', 'BMW iX3', 'Citroen e-C3', 'Zeekr 7X Long Range RWD', 'Renault Zoe ZE50 R110', 'Volkswagen ID.7 Pro', 'Mini Cooper SE', 'MG ZS EV Long Range', 'Skoda Enyaq 85', 'Audi A6 Sportback e-tron performance', 'XPENG G6 RWD Long Range', 'Leapmotor T03', 'Mercedes-Benz EQA 250', 'Peugeot e-3008 97 kWh Long Range', 'Audi Q4 e-tron 40', 'Volkswagen ID.3 Pro', 'Nissan Ariya 87kWh', 'Audi Q6 e-tron quattro', 'Volvo ES90 Twin Motor', 'Ford Explorer Extended Range RWD', 'Rolls-Royce Spectre', 'BYD TANG', 'Kia e-Niro 64 kWh', 'Lynk&Co 02', 'Fiat Grande Panda', 'Renault 4 E-Tech 52kWh 150hp', 'Hongqi E-HS9 99 kWh', 'BMW i5 eDrive40 Sedan', 'Citroen e-C4', 'Opel Corsa-e', 'Mercedes-Benz G 580', 'Dacia Spring Electric 45', 'Kia EV9 99.8 kWh AWD', 'Dongfeng Box 42.3 kWh', 'Polestar 2 Long Range Single Motor', 'Volvo EX40 Single Motor ER', 'Polestar 4 Long Range Single Motor', 'Peugeot e-208', 'Porsche Macan 4 Electric', 'MG MG5 Electric Long Range', 'Lexus RZ 450e', 'Jeep Avenger Electric', 'XPENG G9 RWD Long Range', 'Audi Q8 e-tron 55 quattro', 'Mazda MX-30', 'Honda e:Ny1', 'Lucid Air Dream Edition R', 'BMW i7 xDrive60', 'Opel Grandland 73 kWh', 'Peugeot e-5008 73 kWh', 'Zeekr 001 Performance AWD', 'Leapmotor C10', 'NIO ET5 Long Range', 'Smart EQ fortwo coupe', 'DS N°8 AWD Long Range', 'Peugeot e-2008 SUV', 'Mercedes-Benz EQE 350+', 'CUPRA Tavascan Endurance', 'MG Cyberster GT', 'Opel Mokka-e 50 kWh', 'Voyah Free 106 kWh', 'Honda e', 'Ford Puma Gen-E', 'Volkswagen ID.5 Pro', 'Subaru Solterra AWD', 'Renault Twingo Electric', 'Volkswagen ID. Buzz Pro', 'NIO ET7 Standard Range', 'Ford Capri Extended Range AWD', 'Opel Corsa Electric 51 kWh', 'Smart #3 Brabus', 'Volkswagen e-Up!', 'Volvo EX90 Twin Motor', 'BMW iX2 xDrive30', 'Porsche Taycan 4S', 'Smart #1 Pro+', 'Mercedes-Benz B 250e', 'Volvo XC40 Recharge Pure Electric', 'Maxus MIFA 9', 'Opel Astra Electric', 'Ford Mustang Mach-E ER RWD', 'Fiat 600e', 'Lotus Eletre', 'MG Marvel R', 'Opel Frontera 44 kWh', 'XPENG P7 RWD Long Range', 'BMW i3s 120 Ah', 'Volvo EC40 Single Motor ER', 'Zeekr X Privilege AWD', 'Polestar 3 Long Range Single motor', 'Jaguar I-Pace EV400', 'Omoda E5', 'Lancia Ypsilon', 'NIO EL8 Long Range', 'Peugeot e-308', 'Cadillac Lyriq 600 E4', 'Opel Ampera-e', 'Alfa Romeo Junior Elettrica 54 kWh', 'Seres 3', 'VinFast VF 9 Extended Range', 'Nissan e-NV200 Evalia', 'Mercedes-Benz EQV 300 Long', 'Alpine A290 Electric 220 hp', 'Lexus UX 300e', 'Maserati GranTurismo Folgore', 'Mini Aceman SE', 'Renault Kangoo E-Tech Electric', 'Maserati Grecale Folgore', 'Volvo C40 Recharge Twin Motor', 'Opel Mokka Electric', 'Kia e-Soul 64 kWh', 'Fisker Ocean One', 'Peugeot e-408 58 kWh', 'Ford Focus Electric', 'Lightyear 0', 'Nissan Townstar EV Passenger', 'Aiways U6', 'NIO EL6 Long Range', 'Aiways U5', 'Kia Soul EV', 'Lotus Emeya', 'Toyota PROACE Verso L 75 kWh', 'Smart ForTwo Electric Drive', 'Skoda CITIGOe iV', 'GWM ORA 03 48 kWh', 'Citroen C-Zero', 'NIO EL7 Long Range', 'SsangYong Korando e-Motion', 'Audi SQ6 e-tron', 'Genesis G80 Electrified Luxury', 'Audi S6 Sportback e-tron', 'DS 3 E-Tense', 'Genesis GV60 Premium', 'SEAT Mii Electric', 'Genesis GV70 Electrified Sport', 'Mercedes-Benz eVito Tourer Long 90 kWh', 'Abarth 500e Hatchback', 'e.Go e.wave X', 'Citroen e-Berlingo M 50 kWh', 'Toyota Proace City Verso Electric L1 50 kWh', 'Elaris BEO 86 kWh', 'Mitsubishi i-MiEV', 'Skywell BE11 Long Range', 'Mercedes-Benz EQT 200 Standard', 'Audi SQ8 e-tron', 'Peugeot iOn', 'Opel Vivaro-e Combi M 75 kWh', 'Abarth 600e Scorpionissima', 'Opel Combo-e Life 50 kWh', 'Peugeot e-Expert Combi Standard 75 kWh', 'Maserati GranCabrio Folgore', 'Opel Zafira-e Life L3 75 kWh', 'Peugeot e-Rifter M 50 kWh', 'ORA Funky Cat 48 kWh', 'JAC iEV7s', 'Peugeot Partner Tepee Electric', 'Peugeot e-Traveller L3 75 kWh', 'Citroen e-SpaceTourer XL 50 kWh', 'Citroen e-Jumpy Combi M 75 kWh', 'Smart ForFour Electric Drive', 'Sono Sion', 'Citroen E-Berlingo Multispace', 'Fiat E-Ulysse L2 75 kWh', 'Tesla Cybertruck', 'Hummer EV', 'Xiaomi YU7', 'Xiaomi SU7']

# ✅ Create a mapping: First two words -> Class ID
model_class_mapping = { " ".join(model.split()[:2]): idx for idx, model in enumerate(vehicle_models) }

# ✅ Track incorrect labels
incorrect_labels = []

# ✅ Process each label file
for label_file in os.listdir(LABELS_DIR):
    if not label_file.endswith('.txt'):
        continue

    # Extract first two words from filename
    base_name = os.path.splitext(label_file)[0].replace('_', ' ')  # Convert underscores to spaces
    first_two_words = " ".join(base_name.split()[:2])  # Get only first two words

    expected_class_id = model_class_mapping.get(first_two_words)

    if expected_class_id is None:
        print(f"⚠️ No matching model found for {label_file}. Skipping...")
        continue  # Skip files with no matching model name

    label_path = os.path.join(LABELS_DIR, label_file)

    # Read label file
    with open(label_path, 'r') as f:
        lines = f.readlines()

    # Check class IDs
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue

        actual_class_id = int(parts[0])
        if actual_class_id != expected_class_id:
            incorrect_labels.append((label_file, actual_class_id, expected_class_id))

# ✅ Print summary of incorrect labels
if incorrect_labels:
    print("\n❌ Incorrect Class IDs Found:")
    for file, actual, expected in incorrect_labels:
        print(f"  - {file}: Found {actual}, Expected {expected}")
    print(f"\n🚨 Total Incorrect Labels: {len(incorrect_labels)}")
else:
    print("\n✅ All Class IDs are correct!")

