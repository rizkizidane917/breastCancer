import os
from re import S
from flask import Flask, render_template, request, Response, redirect
import io
import numpy as np
import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)



@app.route('/')
def main():
    return render_template('index.html')
@app.route('/delete')
def delete():
    directory = "./file/"
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    if os.path.isfile('static/plot.png') == True:
        os.remove('static/plot.png')
        plt.clf()
        return redirect('/')
    else:
        return redirect('/')
        pass
    
@app.route('/', methods=['POST','GET'])
def upload():
  
    if os.path.isfile('static/plot.png') == True:
        return redirect('/')
    else:
        try:
            csv_File = request.files['csvFile']
            csv_path = './file/' + csv_File.filename
            csv_File.save(csv_path)
            data = pd.read_csv(csv_path)
            drop_list = ['id','perimeter_mean', 'radius_mean', 'compactness_mean', 'concave points_mean', 'radius_se', 'perimeter_se', 'radius_worst', 'perimeter_worst', 'compactness_worst', 'concavity_worst', 'compactness_se', 'concave points_se', 'texture_worst', 'area_worst']
            data =  data.drop(drop_list, axis=1)

            file = open("my_random_forest.joblib","rb") 
            model = joblib.load(file)
            product_result = model.predict(data)
            product_result = pd.DataFrame(product_result, columns=['diagnosis'])

            m = product_result[product_result['diagnosis'] == 1].count()
            b = product_result[product_result['diagnosis'] == 0].count()
            plot = np.append(m,b)
            c_label = ["Malign (M)" , "Benign (B)"]
            plt.pie(plot , labels = c_label)

            show = plt.savefig('static/plot.png')
          

           
         

        except PermissionError:
            return redirect('/')
    return redirect('/')
if __name__ == '__main__':
    app.run(port=3000, debug=True)