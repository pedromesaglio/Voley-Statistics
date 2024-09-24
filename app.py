from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {
    'admin': {'password': 'admin123', 'name': 'Admin User', 'email': 'admin@example.com', 'stats': pd.DataFrame(), 'court_players': ['']*6},
}


default_stats = pd.DataFrame({
    'Jugador': [''] * 5,
    'Puntos': [0] * 5,
    'Bloqueos': [0] * 5,
    'Servicios': [0] * 5,
    'Errores': [0] * 5,
    'Errores no forzados': [0] * 5
})


class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrecta.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        
        if username in users:
            flash('El usuario ya existe.')
        else:
           
            users[username] = {'password': password, 'name': name, 'email': email, 'stats': default_stats.copy(), 'court_players': ['']*6}
            flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_stats = users[current_user.id]['stats']  
    court_players = users[current_user.id]['court_players']  

    if request.method == 'POST':
        
        for i in range(len(user_stats)):
            user_stats.at[i, 'Jugador'] = request.form[f'jugador_{i}']
            user_stats.at[i, 'Puntos'] = request.form[f'puntos_{i}']
            user_stats.at[i, 'Bloqueos'] = request.form[f'bloqueos_{i}']
            user_stats.at[i, 'Servicios'] = request.form[f'servicios_{i}']
            user_stats.at[i, 'Errores'] = request.form[f'errores_{i}']
            user_stats.at[i, 'Errores no forzados'] = request.form[f'errores_no_forzados_{i}']

       
        new_player = request.form.get('new_player')
        if new_player:
            new_stats = {
                'Jugador': new_player,
                'Puntos': request.form.get('new_puntos', 0),
                'Bloqueos': request.form.get('new_bloqueos', 0),
                'Servicios': request.form.get('new_servicios', 0),
                'Errores': request.form.get('new_errores', 0),
                'Errores no forzados': request.form.get('new_errores_no_forzados', 0)
            }
            user_stats.loc[len(user_stats)] = new_stats

        
        for i in range(6):
            court_players[i] = request.form.get(f'player_pos_{i}', '')

        return redirect(url_for('index'))

    return render_template('index.html', tables=user_stats, titles=user_stats.columns.values, court_players=court_players)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        
        users[current_user.id]['name'] = name
        users[current_user.id]['email'] = email
        flash('Perfil actualizado con éxito.')
        return redirect(url_for('profile'))
    
    user_data = users[current_user.id]
    return render_template('profile.html', name=user_data['name'], email=user_data['email'])

if __name__ == '__main__':
    app.run(debug=True)

