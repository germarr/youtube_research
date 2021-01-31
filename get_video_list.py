from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
import time

## API CALL + MERGE WITH CATEGORY ID + language
def get_videos():
    api_key= input("API_KEY: ")
    youtube = build("youtube","v3", developerKey=api_key)

    date_new= date(datetime.now().year,datetime.now().month,datetime.now().day).isoformat()
    hour=datetime.now().hour
    title=f"{date_new[0:4]}_{date_new[5:7]}_{date_new[8:10]}_{datetime.now().hour}"

    categories = []
    top_videos = []

    chart_mx= youtube.videos().list(
    part=["id","snippet","statistics"],
    chart="mostPopular",
    regionCode="MX",
    maxResults=50).execute()
    
    category_id= youtube.videoCategories().list(
    part=["snippet"],
    regionCode="MX").execute()

    for i in category_id["items"]:
        categories.append({
            "category_id": i["id"],
            "category_title": i["snippet"]["title"]
        })
    
    for i in chart_mx["items"]:
        vid_id=i["id"]
        ytb_link=f"https://youtu.be/{vid_id}"
        tags = None
        language = None

        try:
            i["snippet"]["defaultAudioLanguage"]
        except KeyError:
            language = ""
        
        if language != "":
            language = i["snippet"]["defaultAudioLanguage"]
            
        try:
            i["snippet"]["tags"]
        except KeyError:
            tags = ""

        if tags!="":
            tags = i["snippet"]["tags"]
    
        top_videos.append({
            "published_date":i["snippet"]["publishedAt"],
            "trending_date":f"{date_new}T{hour}:00:00Z",
            "category_id":i["snippet"]["categoryId"],
            "channel_title":i["snippet"]["channelTitle"],
            "tags":tags,
            "video_title":i["snippet"]["title"],
            "views":i["statistics"]["viewCount"], 
            "likes":i["statistics"]["likeCount"],
            "dislikes":i["statistics"]["dislikeCount"],
            "comments":i["statistics"].get("commentCount"),
            "description":i["snippet"]["description"],
            "channel_id":i["snippet"]["channelId"],
            "link":ytb_link,
            "thumbnail":i["snippet"]["thumbnails"]["medium"]["url"],
            "hour_trending":hour,
            "video_lang":language,
            "count": 1
        })

    categories_df = pd.DataFrame.from_dict(categories)
    top_videos_df = pd.DataFrame.from_dict(top_videos)
    df = pd.merge(top_videos_df, categories_df,on ='category_id', how ='inner').to_csv("test_file.csv")

    

if __name__ == "__main__":
    api_testing()


