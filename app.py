from flask import Flask,request,render_template
import data
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/home1')
def home1():
    return render_template('home1.html')
@app.route("/submit",methods=['POST'])
def submit():
    form_data = {
        "longitude": request.form['longitude'],
        "latitude": request.form['latitude'],
        "Housing_median_age": request.form['Housing_median_age'],
        "total_rooms": request.form['Total Rooms'],
        "total_bedrooms": request.form['Total Bedrooms'],
        "Population": request.form['Population'],
        "households": request.form['Household'],
        "median_income": request.form['Median_income'],
        "ocean_proximity": request.form['Ocean-proximity']
    }

    # prepare values for model
    values = [
        float(form_data["longitude"]),
        float(form_data["latitude"]),
        float(form_data["Housing_median_age"]),
        float(form_data["total_rooms"]),
        float(form_data["total_bedrooms"]),
        float(form_data["Population"]),
        float(form_data["households"]),
        float(form_data["median_income"]),
        form_data["ocean_proximity"]
    ]

    result = data.predict_price(values)

    return render_template('home1.html', prediction=result ,form_data=form_data)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
