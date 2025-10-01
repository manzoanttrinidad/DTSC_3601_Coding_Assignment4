import os, pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import json

def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

def main():
    supabase = get_client()

    # Load data from JSON file
    with open("/Users/anthonymanzo-trinidad/Documents/llm_example/soundcloud_trending.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        music_df = pd.DataFrame(data.get("tracks", []))
    
    # Upsert data into Supabase table
    records = music_df.to_dict(orient="records")
    response = supabase.table("soundcloud_tracks").upsert(records).execute()
    print("Upsert response:", response)



main()