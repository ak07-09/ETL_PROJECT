import json 
import pandas as pd
import glob
import os

def transfrom_nasa_data():
    os.makedirs("../data/staged", exist_ok=True)

    latest_file=sorted(glob.glob("../data/raw/nasa_apod_*.json"))[-1]
    
    with open(latest_file, "r") as f:
        data = json.load(f)
       
    df=pd.DataFrame({
        "date": [data["date"]],
        "title": [data["title"]],
        "explanation": [data["explanation"]],
        "url": [data["url"]],
        "hdurl": [data["hdurl"]]
    })

    output_path=f"../data/staged/nasa_apod_cleaned.csv"
    df.to_csv(output_path, index=False)

    print(f"Transformed data saved to: {output_path}\n")

    return df

if __name__ == "__main__":
    transfrom_nasa_data()