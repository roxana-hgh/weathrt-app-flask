from flask import Flask
from flask import render_template, redirect ,url_for, request,flash
import requests , json , datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Weather-app'

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        city = request.form["city"]
        urlt = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=135a45ace75a9630210cb4c07ab478db"
        responses = requests.get(urlt)
        if responses.status_code == 404:
            flash("City not found!","danger")
            return render_template('main.html')
        else:    
            return redirect(url_for('currentWeather',cty=city))
    else:
        return render_template('main.html')

@app.route('/<string:cty>')
def currentWeather(cty):
    cty.lower()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cty}&appid=135a45ace75a9630210cb4c07ab478db"
    response = requests.get(url)
    record = json.loads(response.text)
    weather = record['weather']
    description = weather[0]['description']
    icon = weather[0]['icon']
    iconURL = f"http://openweathermap.org/img/wn/{icon}@4x.png"
    temp = record["main"]
    tempc = int(temp['temp'] - 273.15)
    tempfeels = int(temp["feels_like"] - 273.15)
    humidity = temp['humidity']
    wind = record['wind']
    Wspeed = wind['speed']
    return render_template('current_weather.html',city = cty.capitalize(), weatherd = description.capitalize(), temp = tempc, 
                            feels = tempfeels,wind = Wspeed ,humidity = humidity,icon = iconURL, dt = datetime.datetime.now())

    

    
if __name__ == "__main__":
    app.run(debug=True)