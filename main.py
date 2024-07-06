import json
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from vac_scr import get_vacs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Vacancy {self.keyword}>'

    def set_description(self, vacs):
        self.description = json.dumps(vacs)

    def get_description(self):
        return json.loads(self.description)

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/output')
def output():
    keyword = request.args.get('keyword')
    if keyword:
        keyword = keyword.lower()
        vacancy = Vacancy.query.filter_by(keyword=keyword).first()
        if vacancy:
            vacs = vacancy.get_description()
        else:
            vacs = get_vacs(keyword)
            new_vacancy = Vacancy(keyword=keyword)
            new_vacancy.set_description(vacs)
            db.session.add(new_vacancy)
            db.session.commit()
    else:
        return redirect('/')

    return render_template('output.html',searchBy=keyword, resultsNumber=len(vacs), vacs=vacs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')