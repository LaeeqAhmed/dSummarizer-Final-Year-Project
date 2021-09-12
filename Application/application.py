from flask import Flask
from flask import render_template
from flask import request
import requests
from cv2 import *
import pymongo
from Poster import Poster

app = Flask(__name__, template_folder='template')


def update_movie_posters():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dSummarizerDB = myclient["dSummarizerDB"]
    polarityCollection = dSummarizerDB["polarityCollection"]
    list_of_new_movies = polarityCollection.find({"Year": 2020})
    if list_of_new_movies:
        for i, movies in enumerate(list_of_new_movies):
            print(movies["Name"])
            p = Poster(movies["Name"], None)
            poster_link = p.getPoster()
            r = requests.get(poster_link)
            with open(rf"C:\Users\Shahram\Desktop\FYP\Application\static\images\temp.jpg", 'wb') as f:
                f.write(r.content)
                f.close()
                frame = cv2.imread(rf"C:\Users\Shahram\Desktop\FYP\Application\static\images\temp.jpg")
                HEIGHT = 214
                WIDTH = 154
                frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
                cv2.imwrite(rf"C:\Users\Shahram\Desktop\FYP\Application\static\images\movie{i}.jpg", frame)
            if i == 18:
                break


# update_movie_posters()


@app.route("/")
def home():
    return render_template("updated_index.html")

@app.route("/api/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("POST REQUEST RECIEVED")
        username = request.form.get("username")
        email = request.form.get("email")
        print(username)
        print(email)
        url = "http://127.0.0.1:5000/api/addUser"
        headers = {
            'username': username,
            'email': email
        }
        params = {}
        response = requests.request("POST", url, headers=headers, params=params)
        print(response.status_code)
    elif request.method == "GET":
        return render_template("updated_index.html")
    else:
        return render_template("updated_index.html")
    return render_template("updated_index.html")


@app.route("/result/movie/<string:name>")
def result(name):
    url = "http://127.0.0.1:5000/api/dev/get/polarity"
    headers = {
        'name': name
    }
    params = {}
    response = requests.request("GET", url, headers=headers, params=params)
    # fetching the poster
    poster = Poster(name, response.json()['Year'])
    #  fetching summary Extractive
    # summaryURL = "http://127.0.0.1:5000/api/extractiveSummary"
    # summaryResponse = requests.request("GET", summaryURL, headers=headers, params=params)
    #  fetching summary abstractive
    AsummaryURL = "http://127.0.0.1:5000/api/abstractiveSummary"
    AsummaryResponse = requests.request("GET", AsummaryURL, headers=headers, params=params)
    return render_template("result.html", name=name,
                           img_url=poster.getImage(),
                           year=str(response.json()['Year']).split('.')[0],
                           stars=response.json()['Stars'],
                           pos=response.json()['pos'],
                           neg=response.json()['neg'],
                           posNorm=response.json()['posNorm'],
                           negNorm=response.json()['negNorm'],
                           extsum=AsummaryResponse.json()['Summary']
                           )


@app.route("/aboutUs")
def about():
    return render_template('about.html')


@app.route("/api/retrieve")
def retrieve():
    return render_template('retrieve.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
