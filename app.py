from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Anime(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Mc = db.Column(db.String(200), nullable=False)
    Fc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        Title = request.form['name']
        Mc = request.form['Mc']
        Fc = request.form['Fc']
        anime = Anime(Title = Title, Mc=Mc, Fc=Fc)
        db.session.add(anime)
        db.session.commit()
    all_anime = Anime.query.all()
    return render_template('animehome.html',all_anime=all_anime)

@app.route('/anime')
def anime():
    all_anime = Anime.query.all()
    print(all_anime)
    return "moshi moshi"

@app.route('/delete/<int:Sno>')
def delete_anime(Sno):
    anime = Anime.query.filter_by(Sno=Sno).first()
    db.session.delete(anime)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update_anime(Sno):
    if request.method == 'POST':
        Title = request.form['name']
        Mc = request.form['Mc']
        Fc = request.form['Fc']
        anime = Anime.query.filter_by(Sno=Sno).first()
        anime.Title = Title
        anime.Mc = Mc
        anime.Fc = Fc
        db.session.add(anime)
        db.session.commit()
        return redirect('/')
    anime = Anime.query.filter_by(Sno=Sno).first()
    return render_template('animeupdate.html', anime=anime)

if __name__ == '__main__':
    app.run(debug=True)