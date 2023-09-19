from ctypes.wintypes import tagPOINT
from flask import Flask, render_template, request
import requests as rq
from dotenv import load_dotenv, dotenv_values
import os 

load_dotenv() 
API_KEY = (os.getenv("API_KEY")) #initalizes API key

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    api_url = f'https://api.myanimelist.net/v2/anime?q={search_query}'

    headers = {'X-MAL-CLIENT-ID': API_KEY}  

    response = rq.get(api_url, headers=headers)
    data = response.json() #this is the data we get from the website
    idnum = []

    results = []
    for anime in data['data']:
        idnum.append(anime['node']['id'])  #we need the id number of the anime to get the title, image, and synopses
    
    for ids in idnum:
        synopsis_key = f'https://api.myanimelist.net/v2/anime/{ids}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics' \
        
        response2 = rq.get(synopsis_key, headers=headers)
        data2 = response2.json() #this is the data we get from the website using the ids
        result = {
            'title': data2['title'],
            'image_url': data2['main_picture']['medium'],
            'synopsis': data2['synopsis']
            }
        results.append(result)
    
    return render_template('home.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
