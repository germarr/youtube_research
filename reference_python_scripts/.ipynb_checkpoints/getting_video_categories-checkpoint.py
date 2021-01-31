from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,datetime
import time
import json

def api_testing():
    api_key= ""
    youtube = build("youtube","v3", developerKey=api_key)

    nextPageToken = None
    categories = []

    category_id= youtube.videoCategories().list(
    part=["snippet"],
    regionCode="MX").execute()

    print(json.dumps(category_id, indent=4))

    for i in category_id["items"]:
        categories.append({
            "id": i["id"],
            "category": i["snippet"]["title"]
        })
    
    print(json.dumps(categories, indent=4))

if __name__ == "__main__":
    api_testing()