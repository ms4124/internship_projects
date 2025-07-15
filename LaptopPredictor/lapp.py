from flask import Flask, render_template, request
# import pickle

app = Flask(__name__)

# # Load model
# with open('Lmodel.lb', 'rb') as f:
#     model = pickle.load(f)
import joblib
model = joblib.load('Lmodel.lb')


@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Get form data
#         brand = request.form['brand']
#         processor_brand = request.form['processor_brand']
#         processor_name = request.form['processor_name']
#         processor_gnrtn = request.form['processor_gnrtn']
#         ram_gb = int(request.form['ram_gb'])
#         ssd = int(request.form['ssd'])
#         hdd = int(request.form['hdd'])
#         graphic_card_gb = int(request.form['graphic_card_gb'])
#         warranty = int(request.form['warranty'])
#         touchscreen = int(request.form['Touchscreen'])  # 1 for Yes, 0 for No
#         rating = float(request.form['rating'])

#         # Combine all features into a list
#         features = [[brand, processor_brand, processor_name, processor_gnrtn,
#                      ram_gb, ssd, hdd, graphic_card_gb, warranty, touchscreen, rating]]

#         # Predict
#         prediction = model.predict(features)[0]

#         return render_template('result.html', price=round(prediction, 2))

#     except Exception as e:
#         return f"Error: {e}"
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Convert all form inputs properly
        brand = int(request.form['brand'])
        processor_brand = int(request.form['processor_brand'])
        processor_name = int(request.form['processor_name'])
        processor_gnrtn = int(request.form['processor_gnrtn'])
        ram_gb = int(request.form['ram_gb'])
        ssd = int(request.form['ssd'])
        hdd = int(request.form['hdd'])
        graphic_card_gb = int(request.form['graphic_card_gb'])
        warranty = int(request.form['warranty'])
        touchscreen = int(request.form['Touchscreen'])  # 1 for Yes, 0 for No
        rating = float(request.form['rating'])

        # Feature list
        features = [[brand, processor_brand, processor_name, processor_gnrtn,
                     ram_gb, ssd, hdd, graphic_card_gb, warranty, touchscreen, rating]]

        # Predict
        prediction = model.predict(features)[0]

        return render_template('result.html', price=round(prediction, 2))

    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

