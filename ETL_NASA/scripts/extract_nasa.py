import json
from pathlib import Path
from datetime import datetime
import requests

DATA_DIR = Path(__file__).resolve().parents[1]/"data"/"raw"
DATA_DIR.mkdir(parents = True, exist_ok = True)

def extract_nasa_data() :
    url = "https://api.nasa.gov/planetary/apod?api_key=ai40hxUg7wyFi0B4MT7kidR1IPQPtze3mSpLotHl"
    params = {    
        "date" : datetime.now().strftime("%Y-%m-%d"),
    }
    resp = requests.get(url,params = params)
    resp.raise_for_status()
    data = resp.json()

    filename = DATA_DIR/f"nasa_apod_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filename.write_text(json.dumps(data,indent = 2))
    print(f"Extracted NASA APOD data saved to : {filename}")
    return data

def extract_nasa_image():
    DAT_DIR = Path(__file__).resolve().parents[1]/"data"/"images"
    DAT_DIR.mkdir(parents = True, exist_ok = True)

    url = "https://api.nasa.gov/planetary/apod?api_key=ai40hxUg7wyFi0B4MT7kidR1IPQPtze3mSpLotHl"
    params = {    
        "date" : datetime.now().strftime("%Y-%m-%d"),
    }
    resp = requests.get(url,params = params)
    resp.raise_for_status()
    data = resp.json()

    image_url = data.get("hdurl")
    image_resp = requests.get(image_url)
    image_resp.raise_for_status()

    img_name = DAT_DIR / f"nasa_apod_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    img_name.write_bytes(image_resp.content)
    print(f"Extracted NASA APOD image saved to : {img_name}")
    return img_name

if __name__ == "__main__" : 
    extract_nasa_data()
    extract_nasa_image()