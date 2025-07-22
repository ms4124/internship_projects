from flask import Flask, render_template, request
import joblib
import datetime

app = Flask(__name__)
model = joblib.load('insmodel.lb')

history = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            sex = int(request.form['sex'])
            bmi = float(request.form['bmi'])
            children = int(request.form['children'])
            smoker = int(request.form['smoker'])
            region = int(request.form['region'])

            features = [[age, sex, bmi, children, smoker, region]]
            prediction = model.predict(features)[0]
            prediction = round(prediction, 2)

            # Save to history
            timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            history.append([timestamp, age, sex, bmi, children, smoker, region, prediction])

            return render_template('index.html', prediction=prediction)
        except Exception as e:
            return str(e)
    return render_template('index.html')

@app.route('/history')
def show_history():
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)

