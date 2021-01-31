import pandas as pd
from datetime import datetime,date
import time
import os.path
from os import path

date_new= date(datetime.now().year,datetime.now().month,datetime.now().day).isoformat()
hour=datetime.now().hour
title=f"{date_new[0:4]}_{date_new[5:7]}_{date_new[8:10]}_{datetime.now().hour}"

def merge_day():
    frames=[]

    for i in range(hour):
        if path.exists(f"trending_videos_data/{title[0:11]}{i}.csv"): 
            frames.append(pd.read_csv(f"trending_videos_data/{title[0:11]}{i}.csv", index_col=0))

    main_df = pd.concat(frames).drop_duplicates(subset=['video_title'], keep='last').to_csv("merged_file.csv")


def union():
    frames=[]

    for i in range(hour):
        if path.exists(f"trending_videos_data/{title[0:11]}{i}.csv"): 
            frames.append(pd.read_csv(f"trending_videos_data/{title[0:11]}{i}.csv", index_col=0))

    main_df = pd.concat(frames).to_csv("union_file.csv")

    
if __name__ == "__main__":
    merge_day()
    