import numpy as np
from flask import Flask, request, render_template
import pickle

# Create app object using Flask class
app = Flask(__name__)

# Load trained model (sklearn)
model = pickle.load(open('models/model.pkl', 'rb'))

# Home directory
@app.route('/')
def home():
    return render_template('index.html')

# Prediction
@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    features = np.array(features).reshape(1,-1)
    prediction = model.predict(features)

    output = min(round(prediction[0] / 100, 1), 10.0)
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
        show_results = 1 
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)