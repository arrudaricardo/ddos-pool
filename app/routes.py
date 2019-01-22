from app import app
from flask import render_template
from .models import Pool


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pool/<poolid>')
def get_pool(poolid):
    pool = Pool.query.filter(Pool.id == poolid).first()
    if pool is None:
        return 'page not exist'

    else:
        return render_template('pool.html', pool=pool)
