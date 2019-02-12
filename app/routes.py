from app import app, db, socketio
from .models import Pool
from flask import render_template, request, jsonify, url_for, redirect, Response, send_from_directory, session
from os import listdir, path
from flask_socketio import emit, join_room, leave_room
from random import randint

@app.route('/')
def index():
    # todo: get the last n Pool Create
    last_pools = Pool.query.order_by(Pool.id.desc()).limit(4).all()
    popular_pools = Pool.query.order_by(Pool.number_attackers.desc()).limit(4).all()
    return render_template('index.jinja2', popular_pools=popular_pools, last_pools=last_pools)


@app.route('/pool/<poolid>')
def get_pool(poolid):
    pool = Pool.query.filter(Pool.id == poolid).first()

    session['name'] = 'anon_{}'.format(randint(1000,1000))
    session['room'] = poolid

    if pool is None:
        return 'pool do not exist'
    else:
        return render_template('pool.jinja2', pool=pool)


@app.route('/create', methods=['GET', 'POST'])
def create_pool():
    if request.method == 'GET':

        # send all attack_script in dir to display code
        path_attack_script = path.join(path.dirname(path.abspath(__file__)), "templates", "attack_script")
        attacks_script = list(map(lambda x: x.split('.')[0], listdir(path=path_attack_script)))

        return render_template('createPool.jinja2', attacks_script=attacks_script )
    elif request.method == 'POST':

        # create Pool in DB
        if request.form['terms'] == 'true':
            
            if request.form['attackType'] == 'Custom Code':
                custom_code = request.form['customCode']
                if len(custom_code) > 1000:
                    return jsonify(error='custom code too big')  
            else:
                custom_code = None
                # check attack codes availibles
                path_attack_script = path.join(path.dirname(path.abspath(__file__)), "templates", "attack_script")
                attacks_script = list(map(lambda x: x.split('.')[0], listdir(path=path_attack_script)))
                if request.form['attackType'] not in attacks_script:
                    return jsonify(error='attack_code dont exist')  

            new_pool = Pool(name=request.form['poolName'],
            target_address=request.form['poolTarget'],
            attack_type=request.form['attackType'],
            comment=request.form['poolComment'],
            port=request.form['poolPort'],
            custom_code=custom_code)

            db.session.add(new_pool)
            db.session.commit()

            return redirect(url_for('get_pool', poolid=new_pool.id, code=305))
        else: 
            return jsonify(error='terms')

@app.route('/getAttack', methods=['POST'])
def getAttack():
    """send attack type source code"""
    attack_type = request.form['attackType']
    return send_from_directory('templates/attack_script', filename=attack_type + '.jinja2')


## Socket IO Logic
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""

    room = session.get('room')

    # add number of attackers
    pool = Pool.query.filter(Pool.id == room).first()
    pool.number_attackers += 1
    db.session.commit()

    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the pool.', 'numAttackers': pool.number_attackers}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ': ' + message['msg']}, room=room)



@socketio.on('left', namespace='/chat')
def left(message):
    """ Run when user disconnecto form the room"""
    room = session.get('room')
    leave_room(room)
    # remove number of attackers for the pool
    pool = Pool.query.filter(Pool.id == room).first()
    pool.number_attackers -= 1
    db.session.commit()

    emit('status', {'msg': session.get('name') + ' has left the pool.', 'numAttackers': pool.number_attackers}, room=room)

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    """ Run when user lose connection form the room
    User is unable to call disconnect function in client side since disconnect is special func for losing connection
    """
    room = session.get('room')
    leave_room(room)
    # remove number of attackers for the pool
    pool = Pool.query.filter(Pool.id == room).first()
    pool.number_attackers -= 1
    db.session.commit()

    emit('status', {'msg': session.get('name') + ' has left the pool.', 'numAttackers': pool.number_attackers}, room=room)