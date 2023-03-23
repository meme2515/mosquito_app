import numpy
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

if __name__ == '__main__':
    app.run()