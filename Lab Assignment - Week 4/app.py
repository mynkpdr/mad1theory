from flask import Flask, request, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

app = Flask(__name__)
df = pd.read_csv('data.csv', sep=", ", engine='python')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        df = pd.read_csv('data.csv', sep=", ", engine='python')
        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')
        
        
        if not id_value or not id_type:
            return render_template('error.html', message="Something went wrong")
        
        if id_type == 'student_id':
            data = df[df['Student id'] == int(id_value)]
            if data.empty:
                return render_template('error.html', message="Something went wrong")
            total_marks = data['Marks'].sum()
            return render_template('student.html', data=data.to_dict('records'), total_marks=total_marks)
        
        elif id_type == 'course_id':
            data = df[df['Course id'] == int(id_value)]
            if data.empty:
                return render_template('error.html', message="Something went wrong")
            avg_marks = data['Marks'].mean()
            max_marks = data['Marks'].max()
            plt.hist(data['Marks'], bins=10, edgecolor='black')
            plt.title('Histogram of Marks')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            
            plt.savefig('static/histogram.png')
            plt.close()
        


            return render_template('course.html', avg_marks=avg_marks, max_marks=max_marks )
    
    elif request.method=="GET":
        return render_template('index.html')
    
    return render_template('error.html', message="Something went wrong")
    


if __name__ == '__main__':
    app.run(debug=True)
