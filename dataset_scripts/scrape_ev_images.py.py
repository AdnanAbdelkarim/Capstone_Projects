import os
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

# ✅ Constants
CHROMEDRIVER_PATH = r"C:\Users\student\Desktop\chromedriver.exe"
SAVE_DIR = r"C:\Users\student\Desktop\train\images"
IMAGES_PER_MODEL = 50  # ✅ How many images per vehicle

# ✅ Vehicle models list 
vehicle_models =['Xiaomi SU7']
# ✅ Setup Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def download_images_bing(search_term, save_folder):
    search_url = f"https://www.bing.com/images/search?q={search_term}+car"
    driver.get(search_url)
    time.sleep(3)  # ✅ Give the page time to load

    # ✅ Find all image containers that have high-res URLs inside JSON
    image_containers = driver.find_elements(By.CSS_SELECTOR, "a.iusc")

    print(f"🔎 Found {len(image_containers)} potential images for: {search_term}")

    if len(image_containers) == 0:
        print("❌ No images found.")
        return

    os.makedirs(save_folder, exist_ok=True)
    count = 0

    for idx, container in enumerate(image_containers):
        if count >= IMAGES_PER_MODEL:
            break

        try:
            # ✅ Extract JSON metadata stored in `m` attribute
            metadata = container.get_attribute("m")
            if not metadata:
                continue

            # ✅ Convert JSON to dictionary
            data = json.loads(metadata)
            image_url = data.get("murl")  # High-res image URL

            if not image_url or not image_url.startswith("http"):
                print(f"⚠️ Skipping image {idx} - No valid URL")
                continue

            # ✅ Download and save image
            response = requests.get(image_url, timeout=10)
            img_obj = Image.open(BytesIO(response.content)).convert('RGB')

            file_name = f"{search_term.replace(' ', '_')}_{count + 1}.jpg"
            file_path = os.path.join(save_folder, file_name)
            img_obj.save(file_path)
            print(f"✅ Saved: {file_path} (Resolution: {img_obj.size[0]}x{img_obj.size[1]})")

            count += 1
            time.sleep(1)  # ✅ Small delay to avoid being blocked

        except Exception as e:
            print(f"⚠️ Failed image {idx}: {e}")

    print(f"🎉 Completed {count} images for: {search_term}\n")

# ✅ Start download
for model in vehicle_models:
    download_images_bing(model, SAVE_DIR)

driver.quit()
print("✅ All downloads complete!")
