from time import process_time_ns
from flask import render_template, request, redirect, Flask, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import os
import numpy as np
import pandas as pd


app = Flask(__name__)
if __name__ == "__main__":
    print("DEB")
    app.run(debug=True)


df = pd.DataFrame()
cols = []

@app.route('/', methods=["GET", "POST"])
def index():
    global df
    global cols
    if request.method == 'POST':
        #print("HOLA")
        if request.files:
            uploaded_file = request.files['filename'] # This line uses the same variable and worked fine
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            print("TIPO: " + str(type(filepath)))
            with open(filepath) as file:
                df = pd.read_csv(file)
                for col in df.columns:
                    cols.append(col)
            #return redirect(request.url)        
    return render_template('index.html',cols=cols)

@app.route("/colss" , methods=['GET', 'POST'])
def colss():
    print("PLOT")
    global df
    global cols
    select = request.form.get('dropp')
    select2 = request.form.get('dropp2')
    graph = request.form.get('source')
    
    fig = Figure()
    ax = fig.subplots()
    
    if graph == '0':
        print("LINEAL")
        ax.plot( np.sort( df[str(select)].to_numpy() ) )
        ax.set_xlabel(select)
    if graph == '1':
        print("SCATT")
        ax.scatter(df[str(select)],df[str(select2)])
        ax.set_xlabel(select)
        ax.set_ylabel(select2)
    if graph == '2':
        print("BAR PLT")
        ax.bar(df[str(select)],df[str(select2)])
        ax.set_xlabel(select)
        ax.set_ylabel(select2)
    if graph == '3':
        print("PIE")
        af = df.groupby(select)[select2].count()
        print(type(af))
        
        x = pd.Series(df[select].unique())
        print(type(x))
        ax.pie(af ,labels = x)
        # ax.set_xlabel(select)
        # ax.set_ylabel(select2)
        
    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    data = '<svg' + img.getvalue().split('<svg')[1]
    
    return render_template('index.html',data=data, cols=cols)



app.config['FILE_UPLOADS'] = "C:\\Users\\ignac\\Documents\\WORKS\\ACTUAL\\INOFGRAFIA\\P3\\proy\\"
