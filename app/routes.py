from app import app, db
from .models import Pool
from flask import render_template, request, jsonify, url_for, redirect


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


@app.route('/create', methods=['GET', 'POST'])
def create_pool():
    if request.method == 'GET':
        return render_template('createPool.html')
    elif request.method == 'POST':
        # print(request.form.to_dict())

        # create Pool in DB
        if request.form['terms'] == 'true':
            new_pool = Pool(name=request.form['poolName'], target_address=request.form['poolTarget'],
            attack_type=request.form['attackType'], comment=request.form['poolComment'],
            port=request.form['poolPort'])
            db.session.add(new_pool)
            db.session.commit()
            print(new_pool.id)

            return redirect(url_for('get_pool', poolid=new_pool.id), code=301)
        else:
            return 'erro'

