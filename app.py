from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)


data = {
    'Jugador': ['Juan', 'Pedro', 'Luis', 'Carlos', 'Miguel'],
    'Puntos': [12, 15, 10, 8, 20],
    'Bloqueos': [3, 2, 5, 1, 4],
    'Servicios': [4, 5, 6, 3, 7],
    'Errores': [2, 1, 3, 4, 1]
}

df = pd.DataFrame(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        for i in range(len(df)):
            df.at[i, 'Puntos'] = request.form[f'puntos_{i}']
            df.at[i, 'Bloqueos'] = request.form[f'bloqueos_{i}']
            df.at[i, 'Servicios'] = request.form[f'servicios_{i}']
            df.at[i, 'Errores'] = request.form[f'errores_{i}']
        
        
        return redirect(url_for('index'))

    return render_template('index.html', tables=df, titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)

