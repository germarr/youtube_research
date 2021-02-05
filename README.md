# Analyzing data from the Yotube API 
Youtube is by far my favorite digital platform, and one of the playlists that always catches my attention is the [**trending**](https://www.youtube.com/feed/trending) page. This playlist summarizes what are the "trendiest" videos on the platform, at any given time, and in any country in which youtube has a presence.


I believe that this playlist could be consider a sample of what the general population of a country is consuming in Youtube.  Based on this premise I decided to do some data anlysis on the numbers from this page and see if I could find some interesting insights about it. If you want to read about the results of this research and, my general toughts about the videos that dominate it, check this [**blog post**](https://gmarr.com) on my site. 

If you want to learn how to do your own research on this playlist, or if you want to learn how to retrieve data from Youtube in general, keep reading.

## `research_V1.ipynb`
This jupyter notebook is the main file for the project. All my analysis, code, and explanations are stored in there. 

The file is divided into 3 parts, and I would like to briefly share the first one. This part describes the code and custom functions that I coded to retrieve data from the Youtube API and how to navigate the file structure to manage the data.<p>&nbsp</p>


## **Part 1. Getting The Data**
---
I created this notebook to make the process of getting the data from Youtube and analyze it as seamless as possible. I used data from the current "Trending" page and also, I stored several day’s worth of data from this same page, from several countries.

Here are the steps that need to be followed to get the data:

### **1.1 Download the [google python client](https://github.com/googleapis/google-api-python-client)**

The `google python client` facilitates the interaction with the Youtube API. While it is not mandatory, I used it in yhis project so all my examples will have it.
```console
!pip install google-api-python-client
```

### **1.2 Importing Additional Libraries**
For all the data analysis I used `pandas` which is one the most popular libraries for data manipulation with Python. In addition to pandas I also imported `numpy`, `matplotlib`, and `datetime`

<ins>**Notes:**</ins>
* If you want to learn more about the `pandas` library, like how to download it or how to use it, you can get the 10-minute tutorial [**HERE**](https://pandas.pydata.org/pandas-docs/stable/10min.html)
* [Click here](https://numpy.org/doc/stable/user/quickstart.html) for additional resources about `numpy` 
* [Click here](https://matplotlib.org/3.3.3/tutorials/index.html) for additional resources about `matplotlib`
* [Click here](https://pypi.org/project/DateTime/) for additional resources about `datetime` 
* I installed most of these packages using `Anaconda`, which is a Python distribution platform. [Click here](https://www.anaconda.com/products/individual) for additional resources about `Anaconda`

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,date
```

### **1.3 Handling Dates**
I created 4 variables to handle all things related to dates. These variables are used all throughout the notebook so it's important to keep them at the global scope.

<ins>**Notes**</ins>
* For this project I used current data from the Youtube trending page and also, I used stored data from this same page.
* Understanding the structure of the `title` and `title_v` variable is key to navigate the stored data files. Attached to this project there's a folder called `trending_videos_data`. This directory manages all the data from each of the countries that are being analyzed. Inside each country, there are 12 folders, each for every month of the year, and each of these folders has a subfolder with each of the days of the month. 


```python
# date_new gets the current date in the isoformat. 
date_new= date(datetime.now().year,datetime.now().month,datetime.now().day).isoformat()

# title gets the date in this format "2021_02_02_10"
title=f"{date_new[0:4]}_{date_new[5:7]}_{date_new[8:10]}_{datetime.now().hour}"

# title_v gets the date in this format "2021_02_02". It's very similar to the result of "date_new" however all the date is separated with a underscore "_".
title_v=f"{date_new[0:4]}_{date_new[5:7]}_{date_new[8:10]}"

#Hour stores the current hour of the day
hour=datetime.now().hour
```

### **1.4 Helper Functions**
I created A Python helper file called `custom_functions.py`. This file handles the functions that are required to get all the videos from the Trending page of a country. Import the file as `cf`.

```python
import custom_functions as cf
```

### **1.5 Current Trending Videos.**
To get the current `Trending` videos on Youtube from any region. Use the `gevideos()` method from the `custom_functions` file. This method requires 2 parameters: 

* `date_new`= We can assign the ` date_new` variable that we declared in our dates variables.
* `hour`= We can assign the ` hour` variable that we declared in our dates variables.

In addition to these parameters, the function will ask for 2 inputs. The `API_Key` and the `CountryCode`. 

* <ins>Notes:</ins>
    * The `API_KEY` refers to the [**Youtube API key**](https://developers.google.com/youtube/v3/getting-started). This key will help us to do requests to Youtube and retrieve data for analysis. To get this key I recommend following this [**tutorial**](https://developers.google.com/youtube/registering_an_application).
    *  Each country that has access to Youtube shows different `Trending` videos. When the `CountryCode` is requested add the 2 letter abbreviation of the country you wish to get the data from. [Here's](https://www.iso.org/iso-3166-country-codes.html) a list of country’s abbreviations.


```python
#Add a variable and assign it the value that is returned from the getvideos() method.

trending_video = cf.getvideos(date_new, hour)
```

### **1.6 Features of the Dataframe.**
The `getvideos()` function will return a dataframe that includes key information about the videos that are currently trending in a country. The Features that this dataframe have are:

* `published_date`: the date that the video was published by the Youtube channel.
* `trending_date`: the date on which the video was trending on the Youtube "Trending" page.
* `category_id`: the category of the video. To learn more about the Youtube categories visit this [link](https://developers.google.com/youtube/v3/docs/videoCategories). 
* `channel_title`: The title of the channel that published the video.
* `tags`: A list of tags that the video included.  
* `video_title`: The title of the video.
* `views`: How many views does this video currently have. 
* `likes`: How many likes does this video currently have.
* `dislikes`: How many dislikes does this video currently have.
* `comments`: How many comments does this video currently have.
* `description`: What's the description that the author of the video included.
* `channel_id`: The id of the channel that published the video. This can serve as a "Unique ID".
* `link`: The link of the video.
* `thumbnail`: A link to the thumbnail of the video on a 320x180px size.
* `hour_trending`: The hour in which this video was trending.
* `video_lang`: If the author of the video included a language for the video it will appear here.
* `count`: A value of 1. I use this feature to do some of the analysis. This feature is not part of the Youtube API.
* `country`: The country in which the video was trending. 
* `category_title`: What's the category of the video. To learn more about the Youtube categories visit this [link](https://developers.google.com/youtube/v3/docs/videoCategories).

```python
trending_videohead(3)
```

### **1.7 `Merge` & `Union` files.**
To perform a deeper analysis I downloaded several days worth of data. To get a better picture of what's trending during the day on youtube I decided to collect the trending page data every hour. Once I had the data for every single hour I created two files from it, the `merge` and the `union` files. 
* For the `merge` file I merged all the files that are created every hour into a single dataframe. Then I drop the duplicates of the dataframe and keep the last appearance of the video. By doing this I end up with all the videos that trended throughout the day.
* For the `union` file I merged all the files that are generated every hour into a single file. Having this dataframe helped me to look for the performance of a video throughout the day (or even several days). 

Both the `merge` and `union` files and can be located inside the folder for each individual day. This is an example of the path to reach the files: 
* `trending_videos_data/CL/02/2021_02_02/union_file.csv`
* `trending_videos_data/CL/02/2021_02_02/merged_file.csv`

```python
# Example of the Union/Merge files of Argentina for February 2, 2021.

uninon_file_ar = pd.read_csv("trending_videos_data/CL/02/2021_02_01/union_file.csv", index_col=0)
merge_file_ar= pd.read_csv("trending_videos_data/CL/02/2021_02_01/merged_file.csv", index_col=0)

# Counting how many videos each of this file contains.
print(f"The union file contains {uninon_file_ar.count()['count']} videos.")
print(f"The merged file contains {merge_file_ar.count()['count']} videos.")
```

### **1.8 `Merge` & `Union` method.**

To get the **daily** `merge` or `union` file from all the countries, call the `daily_file_from()` method from the `cf` library.
* This function returns a dataframe that merges all the union/merge files from the specified countries.
* This functions accepts the next parameters:
    * `get_country` : A list with all the countries that we want to merge. Example: ["BR", "MX", "US"] or ["AR"].
    * `current_day` : This parameter accepts an integer from 1 to 31. Te default value is the result from this function `datetime.now().day`
    * `current_month`  : This parameter accepts an integer from 1 to 12. Te default value is `None`.
    * `type_of_file` : This parameter accepts the strings `merged` or `union`. The default value is `union`
```python
# Example of Union/merge file from all the countries for February 1, 2021.

todays_countries_merged_file= cf.daily_file_from(get_country= ["CL"], current_day=1, current_month=2)
```
To get the **monthly** `merge` or `union` file from all the countries, call the `monthly_file_from()` method from the `cf` library.
* These functions return a dataframe that merges all the countries union/merge file from the current month.
* This functions accepts the next parameters:
    * `get_country` : A list with all the countries that we want to merge. Example: ["BR", "MX", "US"] or ["AR"]
    * `current_month`  : This parameter accepts an integer from 1 to 12. Te default value is None.
    * `type_of_file` : This parameter accepts the strings `merged` or `union`. The default value is `union`

```python
# Example of the "merged" file from 3 countries during February

monthly_countries_union_file= cf.monthly_file_from(get_country= ["ES","BR","CA"], type_of_file="union")
```
