import pandas as pd
import os
from extract_titanic import extract_data

def transform_data(raw_path):
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_dir=os.path.join(base_dir,"data","staged")

    os.makedirs( staged_dir, exist_ok= True )

    df=pd.read_csv(raw_path)

    #1. HANDLING MISSING VALUES

    numeric_cols= ["age","fare"]

    #filling the missing values with median
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    categorical_cols = ["sex", "embarked", "class", "alone", "who"]
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])


    # 2. Feature Engineering

    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["is_child"] = (df["age"] < 12).astype(int)
    df["fare_per_person"] = df["fare"] / df["family_size"]

    
    # 3. Drop unnecessary columns 

    df.drop( columns=["deck", "embark_town"], inplace = True , errors= "ignore")

    # 4. Saved data

    staged_path = os.path.join( staged_dir,"titanic_transformed.csv")

    df.to_csv(staged_path,index=False)

    print(f"DATA TRANSFORMED AND SAVED AT {staged_path}")

    return staged_path


if __name__ == "__main__":

    #form extract_iris import extract_data

    raw_path = extract_data()

    transform_data(raw_path)

   

