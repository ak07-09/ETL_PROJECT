import os
import time
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Initialize the Supabase client
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def load_nasa_to_supabase():
    csv_path = "../data/staged/nasa_apod_cleaned.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing file: {csv_path}")

    df = pd.read_csv(csv_path)

    batch_size = 20

    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]

        # Convert NaN -> None
        batch = batch_df.where(pd.notnull(batch_df), None).to_dict("records")

        values = []
        for r in batch:
            # Safely handle None and escape single quotes for SQL
            date = (r.get("date") or "")
            url = (r.get("url") or "").replace("'", "''")
            title = (r.get("title") or "").replace("'", "''")
            explanation = (r.get("explanation") or "").replace("'", "''").replace("\n", " ")
            hdurl = (r.get("hdurl") or "").replace("'", "''")
            copyright_ = (r.get("copyright") or "").replace("'", "''")

            values.append(
                "("
                f"'{date}', "
                f"'{url}', "
                f"'{title}', "
                f"'{explanation}', "
                f"'{hdurl}', "
                f"'{copyright_}'"
                ")"
            )

        insert_sql = (
            "INSERT INTO nasa_apod "
            "(date, url, title, explanation, hdurl, copyright) "
            f"VALUES {','.join(values)};"
        )

        # Execute the raw SQL via your RPC
        supabase.rpc("execute_sql", {"query": insert_sql}).execute()

        print(f"Inserted rows {i + 1} → {min(i + batch_size, len(df))}")
        time.sleep(0.5)

    print("Finished loading NASA APOD data.")


if __name__ == "__main__":
    load_nasa_to_supabase()
