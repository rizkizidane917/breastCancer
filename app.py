import os
import numpy as np
import joblib
from openpyxl.workbook import workbook
import pandas as pd
import matplotlib
from pandas.core.frame import DataFrame
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main(): 
    return render_template('index.html')

@app.route('/classification', methods=['GET'])
def classification():
    return render_template('classification.html')

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
        return redirect('/classification')
    else:
        return redirect('/classification')
        pass

#API INPUTs
@app.route('/classification', methods=['POST'])
def insertData():
    try :
        csv_File = request.files['csvFile']
        csv_path = './file/' + csv_File.filename
        csv_File.save(csv_path)
        dt = pd.read_csv(csv_path)
        data = dt
        drop_list = ['id','perimeter_mean', 'radius_mean', 'compactness_mean', 'concave points_mean', 'radius_se', 'perimeter_se', 'radius_worst', 'perimeter_worst', 'compactness_worst', 'concavity_worst', 'compactness_se', 'concave points_se', 'texture_worst', 'area_worst']
        data =  data.drop(drop_list, axis=1)

        file = open("my_random_forest.joblib","rb") 
        model = joblib.load(file)
        product_result = model.predict(data)
        product_result = pd.DataFrame(product_result, columns=['diagnosis'])
        # total prod
        df = pd.DataFrame(data).count(axis=1)
        totals = df.index
        totals = [len(totals)]
        print(type(totals))

        accurasi = '94%'
        print(type(accurasi))

        m = product_result[product_result['diagnosis'] == 1].count()
        b = product_result[product_result['diagnosis'] == 0].count()
        plot = np.append(m,b)
        c_label = ["Malign (M)" , "Benign (B)"]
        plt.pie(plot , labels = c_label , autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.3) 
        plt.savefig('static/plot.png')
        os.remove(csv_path)
        plt.clf()
        
        generate(dt,product_result,totals)
        return redirect('/classification')
    except PermissionError:
        pass
# GET DATA AND SAVE TO REPORT
def generate(data, label, total_data):
    data = data["id"]

    total_data = pd.DataFrame(total_data)
    label = label.diagnosis.replace([0,1],['B','M'])
    data = pd.concat([data, label,total_data], axis=1)

    data.columns = ['Id', 'Diagnosis','Total Data']
    
    book = load_workbook('Template/Template.xlsx')
    writer = pd.ExcelWriter('Report/Report.xlsx', engine='openpyxl')
    writer.book = book

    writer.sheets = dict((ws.title, ws)for ws in book.worksheets)
    data.to_excel(writer, index=False, startrow=3)
    book.save('Report/Report.xlsx')
    return

# API IMAGE  
@app.route('/image', methods=['GET'])
def getImage():
    filename = 'static/plot.png'
    return send_file(filename, mimetype='image/png')

# API REPORT
@app.route('/report', methods=['GET'])
def generate_report():
    try:
        filename = 'Report/Report.xlsx'
        return send_file(filename, mimetype='text/csv')
    except PermissionError:
        pass
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)



# import os
# from re import S
# from flask import Flask, render_template, request, redirect
# import numpy as np
# import joblib
# import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def main():
#     return render_template('index.html')
# @app.route('/delete')
# def delete():
#     directory = "./file/"
#     files_in_directory = os.listdir(directory)
#     filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
#     for file in filtered_files:
#         path_to_file = os.path.join(directory, file)
#         os.remove(path_to_file)
#     if os.path.isfile('static/plot.png') == True:
#         os.remove('static/plot.png')
#         plt.clf()
#         return redirect('/')
#     else:
#         return redirect('/')
#         pass

# @app.route('/', methods=['POST','GET'])
# def upload():
  
#     if os.path.isfile('static/plot.png') == True:
#         return redirect('/predict')
#     else:
#         try:
#             csv_File = request.files['csvFile']
#             csv_path = './file/' + csv_File.filename
#             csv_File.save(csv_path)
#             data = pd.read_csv(csv_path)
#             drop_list = ['id','perimeter_mean', 'radius_mean', 'compactness_mean', 'concave points_mean', 'radius_se', 'perimeter_se', 'radius_worst', 'perimeter_worst', 'compactness_worst', 'concavity_worst', 'compactness_se', 'concave points_se', 'texture_worst', 'area_worst']
#             data =  data.drop(drop_list, axis=1)

#             file = open("my_random_forest.joblib","rb") 
#             model = joblib.load(file)
#             product_result = model.predict(data)
#             product_result = pd.DataFrame(product_result, columns=['diagnosis'])2

#             m = product_result[product_result['diagnosis'] == 1].count()
#             b = product_result[product_result['diagnosis'] == 0].count()
#             plot = np.append(m,b)
#             c_label = ["Malign (M)" , "Benign (B)"]
#             plt.pie(plot , labels = c_label , autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.3) 

#             show = plt.savefig('static/plot.png')
#         except PermissionError:
#             return redirect('/')
#     return redirect('/')
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)