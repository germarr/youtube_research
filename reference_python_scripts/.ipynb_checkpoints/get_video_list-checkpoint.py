from googleapiclient.discovery import build
from datetime import datetime,date
import pandas as pd

def get_videos():
    
    api_key = input("API KEY: ")
    youtube = build("youtube","v3", developerKey=api_key)

    date_new= date(datetime.now().year,datetime.now().month,datetime.now().day).isoformat()
    hour=datetime.now().hour
    title=f"{date_new[0:4]}_{date_new[5:7]}_{date_new[8:10]}_{datetime.now().hour}"

    top_videos=[]

    chart_mx= youtube.videos().list(
    part=["id","snippet","statistics"],
    chart="mostPopular",
    regionCode="MX",
    maxResults=50).execute()
    
    for i in chart_mx["items"]:
        vid_id=i["id"]
        ytb_link=f"https://youtu.be/{vid_id}"
        tags = None
        
        try:
            i["snippet"]["tags"]
        except KeyError:
            tags = "No Tags"
        
        if tags!="No Tags":
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
            "thumbnail":i["snippet"]["thumbnails"]["medium"]["url"]
        })    
    print(title)
    pd.DataFrame.from_dict(top_videos).to_csv(f"trending_videos_data/{title}.csv")    

if __name__ == "__main__":
    get_videos()