from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
import time
import os.path
from os import path

c = ["AR","BR","CA","CL","CO","ES","MX","US"]

## API CALL + MERGE WITH CATEGORY ID + language
def getvideos(date_new,hour):
    api_key= input("API_KEY: ")
    country_code = input("CountryCode: ")
    youtube = build("youtube","v3", developerKey=api_key)
 
    categories = []
    top_videos = []

    chart_mx= youtube.videos().list(
    part=["id","snippet","statistics"],
    chart="mostPopular",
    regionCode=country_code,
    maxResults=50).execute()

    category_id= youtube.videoCategories().list(
    part=["snippet"],
    regionCode=country_code).execute()

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
        likes = None
        disLikes= None

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

        try:
            i["statistics"]["likeCount"]
        except KeyError:
            likes = ""

        if likes !="":
            likes = i["statistics"]["likeCount"]

        try:
            i["statistics"]["dislikeCount"]
        except KeyError:
            disLikes = ""

        if disLikes !="":
            disLikes = i["statistics"]["dislikeCount"]
    
        top_videos.append({
            "published_date":i["snippet"]["publishedAt"],
            "trending_date":f"{date_new}T{hour}:00:00Z",
            "category_id":i["snippet"]["categoryId"],
            "channel_title":i["snippet"]["channelTitle"],
            "tags":tags,
            "video_title":i["snippet"]["title"],
            "views":i["statistics"]["viewCount"], 
            "likes":likes,
            "dislikes":disLikes,
            "comments":i["statistics"].get("commentCount"),
            "description":i["snippet"]["description"],
            "channel_id":i["snippet"]["channelId"],
            "link":ytb_link,
            "thumbnail":i["snippet"]["thumbnails"]["medium"]["url"],
            "hour_trending":hour,
            "video_lang":language,
            "count": 1,
            "country":country_code
        })

    categories_df = pd.DataFrame.from_dict(categories)
    top_videos_df = pd.DataFrame.from_dict(top_videos)

    pandas_df = pd.merge(top_videos_df, categories_df,on ='category_id', how ='inner')
    return pandas_df

def plottopics(country_code,date_new,hour):
    api_key= input("API_KEY: ")
    youtube = build("youtube","v3", developerKey=api_key)
 
    categories = []
    top_videos = []

    chart_mx= youtube.videos().list(
    part=["id","snippet","statistics"],
    chart="mostPopular",
    regionCode=country_code,
    maxResults=50).execute()

    category_id= youtube.videoCategories().list(
    part=["snippet"],
    regionCode=country_code).execute()

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
        likes = None
        disLikes= None

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

        try:
            i["statistics"]["likeCount"]
        except KeyError:
            likes = ""

        if likes !="":
            likes = i["statistics"]["likeCount"]

        try:
            i["statistics"]["dislikeCount"]
        except KeyError:
            disLikes = ""

        if disLikes !="":
            disLikes = i["statistics"]["dislikeCount"]
    
        top_videos.append({
            "published_date":i["snippet"]["publishedAt"],
            "trending_date":f"{date_new}T{hour}:00:00Z",
            "category_id":i["snippet"]["categoryId"],
            "channel_title":i["snippet"]["channelTitle"],
            "tags":tags,
            "video_title":i["snippet"]["title"],
            "views":i["statistics"]["viewCount"], 
            "likes":likes,
            "dislikes":disLikes,
            "comments":i["statistics"].get("commentCount"),
            "description":i["snippet"]["description"],
            "channel_id":i["snippet"]["channelId"],
            "link":ytb_link,
            "thumbnail":i["snippet"]["thumbnails"]["medium"]["url"],
            "hour_trending":hour,
            "video_lang":language,
            "count": 1,
            "country":country_code
        })

    categories_df = pd.DataFrame.from_dict(categories)
    top_videos_df = pd.DataFrame.from_dict(top_videos)

    pandas_df = pd.merge(top_videos_df, categories_df,on ='category_id', how ='inner')
    return pandas_df



def merge_day(country,title_v,title,hour):
    frames=[]

    for i in range(hour):
        if path.exists(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/{title[0:11]}{i}.csv"): 
            frames.append(pd.read_csv(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/{title[0:11]}{i}.csv", index_col=0))

    main_df = pd.concat(frames).drop_duplicates(subset=['video_title'], keep='last').to_csv(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/merged_file.csv")
    print("merged_file.csv created!")


def union(country,hour,title_v,title):
    frames=[]

    for i in range(hour):
        if path.exists(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/{title[0:11]}{i}.csv"): 
            frames.append(pd.read_csv(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/{title[0:11]}{i}.csv", index_col=0))

    main_df = pd.concat(frames).to_csv(f"trending_videos_data/{country}/0{datetime.now().month}/{title_v}/union_file.csv")
    print("union_file.csv created!")

    
def todays_folder(title_v):
    parent_dir = "D:/youtube/youtube_research/trending_videos_data/"
    path = os.path.join(parent_dir, title_v) 
    os.makedirs(path) 

    print("Directory '% s' created" % title_v) 
       

if __name__ == "__main__":
    get_videos()
    merge_day()
    union()
    todays_folder()


