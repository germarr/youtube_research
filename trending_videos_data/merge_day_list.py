from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime,date
import time
import json
import os.path
from os import path

frames=[]

for i in range(hour):
    if path.exists(f"trending_videos_data/{title[0:11]}{i}.csv"): 
        frames.append(pd.read_csv(f"trending_videos_data/{title[0:11]}{i}.csv", index_col=0))

main_df = pd.concat(frames).drop_duplicates(subset=['video_title'], keep='last')