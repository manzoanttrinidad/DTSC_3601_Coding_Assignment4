# minimal_soundcloud_gemini.py
import os, json, csv, requests
import google.generativeai as genai
import pandas as pd
import supabase 

URL = "https://soundcloud.com/music-charts-us/sets/artist-pro"
OUT_JSON = "soundcloud_trending.json"
OUT_CSV  = "soundcloud_trending.csv"

# 1) Fetch HTML
html = requests.get(URL, timeout=20).text

# 2) Configure Gemini
genai.configure(api_key="AIzaSyBN6uBAavXYp_B2wAV_TQtekvpsORPo1ow")
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"response_mime_type": "application/json"}  # force JSON back
)

# 3) Ask for strict JSON
system_rules = """You are given raw HTML from SoundCloud Trending.
Extract an object with fields:
{
  "source": "soundcloud_trending",
  "tracks": [
    {
      "title": "<string>" "artist": "<string>",
      "track_url": "<string or empty>",
      "genre": "<string or empty>",
      "plays": null or integer,
      "likes": null or integer,
      "reposts": null or integer
    }
  ]
}
Rules:
- Return ONLY valid JSON (no markdown).
- Missing strings -> "" ; missing numbers -> null.
- Deduplicate by (title, artist, track_url).
"""

resp = model.generate_content([system_rules, html])
data = json.loads(resp.text)  # resp.text is JSON because of response_mime_type

# 4) Save JSON
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("soundcloud_trending.json", "r", encoding="utf-8") as f:
    data = json.load(f)


music_df = pd.DataFrame(data.get("tracks", []))

print(music_df.head())

music_df.to_csv("soundcloud_trending.csv", index=False)




