from flask import Flask ,render_template,request,url_for
import joblib
model = joblib.load("model.lb")
app=Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/project',methods=["POST","GET"])
def predict():
    if request.method=='POST':
        
        brand_name=request.form['brand_name']
        owner=request.form['owner']
        age=request.form['age']
        power=request.form['power']
        km_driven=request.form['kms_driven']
        # print(brand_name,age,owner,km_driven,power)
        brand_dict = {
    'TVS':1,
    'Royal Enfield':2,
    'Triumph':3,
    'Yamaha':4,
    'Honda':5,
    'Hero':6,
    'Bajaj':7,
    'Suzuki':8,
    'Benelli':9,
    'KTM':10,
    'Mahindra':11,
    'Kawasaki':12,
    'Ducati':13,
    'Hyosung':14,
    'Harley-Davidson':15,
    'Jawa':16,
    'BMW':17,
    'Indian':18,
    'Rajdoot':19,
    'LML':20,
    'Yezdi':21,
    'MV':22,
    'Ideal':23
}
        brand_name=brand_dict[brand_name]
        print(brand_name,age,owner,km_driven,power)
        lst=[[brand_name,age,owner,km_driven,power]]
        pred =model.predict(lst)
        print("prediction:-",pred)
    return render_template('project.html')


if __name__ =="__main__":
    app.run(debug=True)

