# @app.route('/', methods=['POST'])
# def predict():
#    csv_File = request.files['csvFile']
#    csv_path = './file/' + csv_File.filename
#    csv_File.save(csv_path)
#    data = pd.read_csv(csv_path)
#    drop_list = ['id','perimeter_mean', 'radius_mean', 'compactness_mean', 'concave points_mean', 'radius_se', 'perimeter_se', 'radius_worst', 'perimeter_worst', 'compactness_worst', 'concavity_worst', 'compactness_se', 'concave points_se', 'texture_worst', 'area_worst']
#    data =  data.drop(drop_list, axis=1)
  
#    file = open("my_random_forest.joblib","rb") 
#    model = joblib.load(file)
#    #data = data.head()
#    #data = data.to_numpy()
#    #print(data)
#    product_result = model.predict(data)
#    product_result = pd.DataFrame(product_result, columns=['diagnosis'])
  
#    m = product_result[product_result['diagnosis'] == 1].count()
#    b = product_result[product_result['diagnosis'] == 0].count()
#    plot = np.append(m,b)
#    c_label = ["Malign (M)" , "Benign (B)"]
#    plt.pie(plot , labels = c_label)
#    plt.show()
  

#    return render_template('index.html')