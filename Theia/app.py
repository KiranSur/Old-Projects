from flask import Flask, redirect, url_for, render_template, request
from cat_clust import getRatings

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/map.html")
def map():
    return render_template("country_map.html")

@app.route("/countymap.html", methods = ['GET', 'POST'])
def counties():
    print(request.method)
    if request.method == 'POST':
        myArr = request.form.getlist('selfeatures')
        count = 0
        hold = []
        while(count < len(myArr)):
            if(myArr[count] == "poptrend"):
                hold.extend([0,5,6,7,8,9,15])
            if(myArr[count] == "education"):
                hold.extend([1,2,3,4])
            if(myArr[count] == "econstat"):
                hold.extend([10,11,14,24,25,26,27,28])
            if(myArr[count] == "racdemo"):
                hold.extend([18,19,20,21,22,23])
            if(myArr[count] == "housing"):
                hold.extend([29])
            count+=1
        hold.sort()
        getRatings(hold,1,"clusts.csv")
        return render_template('countycategories.html')
    else: return render_template('countymap.html')

@app.route("/countycategories.html", methods = ['GET', 'POST'])
def categories():
    print(request.method)
    if request.method == 'POST':
        myArr = request.form.getlist('selfeatures')
        count = 0
        hold = []
        while(count < len(myArr)):
            if(myArr[count] == "poptrend"):
                hold.extend([0,5,6,7,8,9,15])
            if(myArr[count] == "education"):
                hold.extend([1,2,3,4])
            if(myArr[count] == "econstat"):
                hold.extend([10,11,14,24,25,26,27,28])
            if(myArr[count] == "racdemo"):
                hold.extend([18,19,20,21,22,23])
            if(myArr[count] == "housing"):
                hold.extend([29])
            count+=1
        hold.sort()
        getRatings(hold,1,"clusts.csv")
        return render_template('countycategories.html')
    else: return render_template('countycategories.html')

# @app.route('/categories.html', methods=['GET', 'POST'])
# def categories():
#     print(request.form)
#     if "educ" in request.form:
#         print("educ!!!!")
#         getRatings([1,2,3,4],1,"clusts.csv")
#         return render_template('county_categories.html')
#     elif "econ" in request.form:
#         print("econ")
#         getRatings([0,10,11,14, 24, 25, 26, 27, 28, 29],1,"clusts.csv")
#         return render_template('county_categories.html')
#     elif "covid" in request.form:
#         getRatings([0],1,"clusts.csv")
#         return render_template('county_categories.html')
#     elif "demo" in request.form:
#         getRatings([7,8,9,15,18,19,20,21,22,23],1,"clusts.csv")
#         return render_template('county_categories.html')
#     return render_template('categories.html')

if __name__ == "__main__":
    app.run(debug=True)
