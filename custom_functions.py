from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
import time
import os.path
from os import path

c = ["AR","BR","CA","CL","CO","ES","MX","US"]

def main():
    get_videos()
    merge_day()
    union()
    todays_folder()
    monthly_union_file_all_countries()
    monthly_merge_file_all_countries()
    daily_union_file_all_countries()
    daily_merged_file_all_countries()
    monthly_union_file_from(get_country)
    monthly_merged_file_from(get_country)
    daily_union_file_from(get_country)
    daily_merged_file_from(get_country)

## API CALL + MERGE WITH CATEGORY ID + language
def getvideos(date_new,hour):
    api_key= input("API_KEY: ")
    country_code = input("CountryCode: ")
    youtube = build("youtube","v3", developerKey=api_key)
 
    categories = []
    top_videos = []

    chart_mx= youtube.videos().list(
    part=["id","snippet","statistics","contentDetails"],
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
            "duration":i["contentDetails"]["duration"],
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
    


def monthly_file_from(get_country,current_month = None, type_of_file="union"):
    g=[]
    c = get_country
    
    ## MONTH VALIDATION
    if (datetime.now().month < 10) & (current_month == None):
        current_month=f"0{datetime.now().month}"
        
    elif current_month < 10:
        current_month=f"0{current_month}" 

    for countries in range(len(c)):
        country= c[countries]
        for days in range(31):
            if days < 10:
                if path.exists(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_0{days}/{type_of_file}_file.csv"): 
                    g.append(pd.read_csv(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_0{days}/{type_of_file}_file.csv", index_col=0))
            else:
                if path.exists(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_{days}/{type_of_file}_file.csv"): 
                    g.append(pd.read_csv(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_{days}/{type_of_file}_file.csv", index_col=0))
    
    return pd.concat(g)



def daily_file_from(get_country, current_day = datetime.now().day, current_month = None, type_of_file="union"):
    g=[]
    c = get_country
    
    ## MONTH VALIDATION
    if (datetime.now().month < 10) & (current_month == None):
        current_month=f"0{datetime.now().month}"
        
    elif current_month < 10:
        current_month=f"0{current_month}"     
    
    ## DAILY VALIDATION
    if current_day < 10:
        current_day=f"0{current_day}"
    
    for countries in range(len(c)):
        country= c[countries]
            
        if path.exists(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_{current_day}/{type_of_file}_file.csv"):
            g.append(pd.read_csv(f"trending_videos_data/{country}/{current_month}/2021_{current_month}_{current_day}/{type_of_file}_file.csv", index_col=0))

    return pd.concat(g)

       

if __name__ == "__main__":
    main()

