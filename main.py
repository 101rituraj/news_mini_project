from flask import Flask, render_template,request
import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

# api endpoint
HEADLINE_ENDPOINT = "https://gnews.io/api/v4/top-headlines"
SEARCH_ENDPOINT = "https://gnews.io/api/v4/search"

API_KEY = os.environ.get("API_KEY")

HEADERS = {
            "X-Api-Key" : API_KEY
        }

app = Flask(__name__)

# supported countries that are mentioned in api documentation
SUPPORTED_COUNTRIES = {
    "argentina": "ar",
    "australia": "au",
    "austria": "at",
    "bangladesh": "bd",
    "belgium": "be",
    "botswana": "bw",
    "brazil": "br",
    "bulgaria": "bg",
    "canada": "ca",
    "chile": "cl",
    "china": "cn",
    "colombia": "co",
    "cuba": "cu",
    "czechia": "cz",
    "egypt": "eg",
    "estonia": "ee",
    "ethiopia": "et", 
    "finland": "fi",
    "france": "fr",
    "germany": "de",
    "ghana": "gh",
    "greece": "gr",
    "hongkong": "hk",
    "hungary": "hu",
    "india": "in",
    "indonesia": "id",
    "ireland": "ie",
    "israel": "il",
    "italy": "it",
    "japan": "jp",
    "kenya": "ke",
    "latvia": "lv",
    "lebanon": "lb",
    "lithuania": "lt",
    "malaysia": "my",
    "mexico": "mx",
    "morocco": "ma",
    "namibia": "na",
    "netherlands": "nl",
    "newzealand": "nz",
    "nigeria": "ng",
    "norway": "no",
    "pakistan": "pk",
    "peru": "pe",
    "philippines": "ph",
    "poland": "pl",
    "portugal": "pt", 
    "romania": "ro", 
    "russia": "ru",
    "saudiarabia": "sa",
    "senegal": "sn",
    "singapore": "sg",
    "slovakia": "sk",
    "slovenia": "si",
    "southafrica": "za",
    "southkorea": "kr",
    "spain": "es",
    "sweden": "se",
    "switzerland": "ch",
    "taiwan": "tw",
    "tanzania": "tz",
    "thailand": "th",
    "turkey": "tr",
    "uganda": "ug",
    "ukraine": "ua", 
    "unitedarabemirates": "ae",
    "unitedkingdom": "gb",
    "unitedstates": "us",
    "venezuela": "ve",
    "vietnam": "vn", 
    "zimbabwe": "zw"
}

SUPPORTED_COUNTRIES_REVERSE = {code : country for country, code in SUPPORTED_COUNTRIES.items()}

# supported categories that are mentioned in api documentation
SUPPORTED_CATEGORIES = ["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]

@app.route("/", methods=["POST", "GET"])
def select_news_home() :
    if request.method == "GET" :
        #today's date
        today_date = datetime.datetime.now().date() 

        #date, 30 days before from today
        past_date = today_date - datetime.timedelta(days=30)

        return render_template("index.html", contents=None, today_date=today_date, past_date=past_date)

    if request.method == "POST" :
        # getting country from form input
        user_country = request.form.get("country").strip().replace(" ", "").lower()

        # getting category from form input
        user_category = request.form.get("category").strip().replace(" ", "").lower()

        # getting from_date from form input
        from_date = request.form.get("from_date")

        # getting past_date from form input
        to_date = request.form.get("to_date")

        # if user didn't specified from_date
        if from_date :
            from_date = f"{from_date}T00:00:00Z"
        else :
            from_date = None    

        # if user didn't specified to_date
        if to_date :
            to_date = f"{to_date}T23:59:59Z"
        else :
            to_date = None        

        # if user didn't mentioned any categories, then set category to general
        if not user_category :
            user_category = "general"

        # if user didn't mentioned any country, then set country to india
        if not user_country :
            user_country = "india"    

        # country entered by user not in supported country
        if user_country not in SUPPORTED_COUNTRIES :
            return "<h1> no such country found, perhaps you spelled the country wrong </h1>" 

        # category enetred by user not in supported category
        if user_category not in SUPPORTED_CATEGORIES :
            return f"<h1> no '{user_category}' category is supported, you can leave category blank default category is 'General'."

        # required parameters from api documentation
        params = {
            "country" : SUPPORTED_COUNTRIES[user_country],
            "category" : user_category,
            "lang" : "en",
            "from" : from_date,
            "to" : to_date,
        }

        #today's date
        today_date = datetime.datetime.now().date() 
        
        #date, 30 days before from today
        past_date = today_date - datetime.timedelta(days=30)

        # calling top headline api
        response = requests.get(url=HEADLINE_ENDPOINT, params=params, headers=HEADERS)

        if response.status_code == 200 :
            contents = response.json()
            return render_template("index.html", contents=contents, category=user_category, today_date=today_date, past_date=past_date)
        else :
            return f"<h1> Error code : {response.status_code}"

@app.route("/search_news_headlines", methods=["GET", "POST"])
def search_news_home() :
    if request.method == "GET" :
        return render_template("search.html", contents=None)
    
    if request.method == "POST" :
        # getting search keyword from form input
        querry = request.form.get("querry").strip().title()

        # getting country from form input
        user_country = request.form.get("country").strip().replace(" ", "").lower()

        # if user didn't mentioned any country, then set country to india
        if not user_country :
            user_country = "india"    
        
        # country entered by user not in supported country
        if user_country not in SUPPORTED_COUNTRIES :
            return "<h1> no such country found, perhaps you spelled the country wrong </h1>"

        params={
            "q" : querry,
            "country" : user_country,
            "lang" : "en",
        }

        # calling search api
        response = requests.get(url=SEARCH_ENDPOINT, params=params, headers=HEADERS)

        if response.status_code == 200 :
            contents = response.json()
            return render_template("search.html", contents=contents, country=SUPPORTED_COUNTRIES_REVERSE)
        else :
            return f"<h1> Error code : {response.status_code}"

if __name__ == "__main__" :
    app.run(debug=True)