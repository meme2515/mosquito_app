from flask import Flask, request, render_template
from src.weather_api import api_call
from datetime import datetime
import numpy as np
import pickle

# Create app object using Flask class
app = Flask(__name__)

# Load trained model (sklearn)
model = pickle.load(open('src/model.pkl', 'rb'))

# Home directory
@app.route('/')
def home():
    return render_template('index.html')

# Prediction
@app.route('/predict', methods=['POST'])
def predict():
    loc1, loc2, loc3 = request.form.values()

    if (loc1 == "") | (loc2 == "") | (loc3 == ""):
        return render_template('index.html', show_error = 1)

    api_resp = api_call(loc1, loc2, loc3)
    features = [api_resp['rain'], api_resp['min_temp'], api_resp['max_temp']]
    features = np.array(features).reshape(1,-1)
    prediction = model.predict(features)

    output = min(round(prediction[0] / 100, 1), 10.0)
    output = max(output, 0.1)

    if output < 2.0:
        output_class = " (안전)"
    elif output < 4.0:
        output_class = " (주의)"
    elif output < 6.0:
        output_class = " (경계)"
    elif output < 8.0:
        output_class = " (위험)"
    else:
        output_class = " (심각)"

    return render_template(
        'index.html', 
        prediction_text = str(output) + output_class,
        loc1 = loc1,
        loc2 = loc2,
        loc3 = loc3,
        rain = round(api_resp['rain'], 1),
        mintemp = round(api_resp['min_temp'], 1),
        maxtemp = round(api_resp['max_temp'], 1),
        today_year = datetime.today().year,
        today_month = datetime.today().month,
        today_day = datetime.today().day,
        show_results = 1
    )

# run
if __name__ == "__main__":
    app.run(port=8000, debug=True)