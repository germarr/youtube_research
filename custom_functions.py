from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
import time
import os.path
from os import path

c = ["AR","BR","CA","CL","CO","ES","MX","US"]

def main():
    get_videos()
    monthly_file_from(get_country,current_month = None, type_of_file="union")
    daily_file_from(get_country, current_day = datetime.now().day, current_month = None, type_of_file="union")
    stats_from_channel(url=None, channel_id = None)
    get_channel_data(channel_id)

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

def stats_from_channel(url=None, channel_id = None):
    api_key= input("API_KEY: ")
    youtube = build("youtube","v3", developerKey=api_key)
    
    if url == None:
        upload = get_upload_url(channel_id,youtube)
        all_channel_videos= get_playlist_details(upload,youtube)
        return all_channel_videos
    else:
        channel_id= get_channel_id(url,youtube)
        upload = get_upload_url(channel_id,youtube)
        all_channel_videos= get_playlist_details(upload,youtube)
        return all_channel_videos
        
    
def get_channel_id(url,youtube):
    single_video_id = url.split("=")[1].split("&")[0]
    channel_id= youtube.videos().list(part="snippet",id=single_video_id).execute()["items"][0]["snippet"]["channelId"]
    return str(channel_id)

def get_upload_url(channel_id,youtube):
    upload = str(
        youtube.channels().list(
        part="contentDetails",
        id= channel_id
    ).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"])

    return upload

def get_playlist_details(upload,youtube):
    nextPageToken = None
    videos= []

    
    while True:
        vids_ids = []
        pl_request= youtube.playlistItems().list(
        part="contentDetails",
        playlistId=upload,
        maxResults=50,
        pageToken= nextPageToken)
        pl_response = pl_request.execute()
    
        for item in pl_response["items"]:
            vids_ids.append(item["contentDetails"]["videoId"])

        # You get the stats of the first 50 videos.
        vid_request = youtube.videos().list(
            part=["snippet","statistics"],
            id=",".join(vids_ids))
    
        vid_response = vid_request.execute()

    
        for i in vid_response["items"]:
            vid_views = i["statistics"]
            vid_snip = i["snippet"]
            vid_thumb = i["snippet"]["thumbnails"]["medium"]

            vid_id = i["id"]
            yt_lin = f"https://youtu.be/{vid_id}"

            videos.append( 
                {
                    "published":vid_snip.get("publishedAt","0"),
                    "channel_title":vid_snip.get("channelTitle","0"),
                    "title":vid_snip.get("title","0"),
                    "views":int(vid_views.get("viewCount","0")),
                    "likes":int(vid_views.get("likeCount","0")),
                    "dislikes":int(vid_views.get("dislikeCount","0")),
                    "comments":int(vid_views.get("commentCount","0")),
                    "description":vid_snip.get("description","0"),
                    "thumbnails":vid_thumb.get("url","0"),
                    "url" :yt_lin
                }
            )
            
        nextPageToken = pl_response.get("nextPageToken")
        
        if not nextPageToken:
            break
            
    all_channel_videos= pd.DataFrame.from_dict(videos) 
    
    return all_channel_videos

def get_channel_data(channel_id=None, url = None):
    api_key= input("API_KEY: ")
    youtube = build("youtube","v3", developerKey=api_key)
    
    if channel_id == None:
        single_video_id = url.split("=")[1].split("&")[0]
        channel_id= [youtube.videos().list(part="snippet",id=single_video_id).execute()["items"][0]["snippet"]["channelId"]]
    
    empty_list = []

    for ids in range(len(channel_id)):
        channel_stats = youtube.channels().list(
            part=["statistics","snippet","contentDetails"],
            id=channel_id[ids]
            ).execute()
        subscriberCount= None
        country = None
        upload_playlist= None
        
        try:
            channel_stats["items"][0]["statistics"]["subscriberCount"]
        except KeyError:
            subscriberCount = ""
        
        if subscriberCount != "":
            subscriberCount = int(channel_stats["items"][0]["statistics"]["subscriberCount"])
        
        try:
            channel_stats["items"][0]["snippet"]["country"]
        except KeyError:
            country = ""
        
        if country != "":
            country = channel_stats["items"][0]["snippet"]["country"]
            
        try:
            channel_stats["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        except KeyError:
            upload_playlist = ""
        
        if upload_playlist != "":
            upload_playlist= channel_stats["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        empty_list.append({
            "channel_title" : channel_stats["items"][0]["snippet"]["title"],
            "number_of_views": int(channel_stats["items"][0]["statistics"]["viewCount"]),
            "published_videos": int(channel_stats["items"][0]["statistics"]["videoCount"]),
            "channel_subs":subscriberCount,
            "birth_of_channel" : channel_stats["items"][0]["snippet"]["publishedAt"],
            "country":country,
            "upload_playlist":upload_playlist,
            "channel_id":str(channel_id).replace("[","").replace("]","")
        })

    dataframe_output = pd.DataFrame.from_dict(empty_list)

    return dataframe_output

       

if __name__ == "__main__":
    main()

