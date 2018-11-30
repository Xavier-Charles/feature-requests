from flask import Flask, render_template, url_for, flash, redirect, request, session
from requests import app, db, bcrypt
from requests.forms import LoginForm, ClientForm, RequestForm, UpdateClientForm, UpdateRequestForm
from requests.models import User, Requests, Clients
from flask_login import login_user, login_required, current_user, logout_user, login_manager
from operator import attrgetter


@app.route("/", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     flash(f'You are logged in as {current_user.username}!', 'success')
    #     return redirect(url_for('clients'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            # if not is_safe_url(next):
            #     return flask.abort(400)
            flash(f'You are logged in as {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('clients'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', forms=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/clients", methods=['GET', 'POST'])
@login_required
def clients():
    form = ClientForm()
    client_list =Clients.query.all()
    user_id = int(session['user_id'])
    
    if form.validate_on_submit():
        client = Clients(name=form.name.data, location=form.location.data, user_id=user_id)
        db.session.add(client)
        db.session.commit()
        flash(f'{client.name} has been added!', 'success')
        return redirect(url_for('clients'))

    return render_template('clients.html', forms=form, clients=client_list, title='Clients')

# def save_file():

@app.route("/clients/requests/<int:client_id>", methods=['GET', 'POST'])
def requests(client_id):
    form = RequestForm()
    user_id = int(session['user_id'])
    client = Clients.query.get_or_404(client_id)
    request_list = Requests.query.filter_by(client_id=client.id).all()
    request_list.sort(key = attrgetter('client_priority'))
    #  requests=client_requests, add this when done with the form
    # files = url_for('static','files/'+ form.files.data)
    if form.validate_on_submit():
        # if form.files.data: use to check file size
        request = Requests(
                title=form.title.data,
                description=form.description.data,
                client_priority=form.client_priority.data,
                target_date=form.target_date.data,
                files=form.files.data,
                product_area=form.product_area.data,
                client_id= client.id,
                user_id= user_id
                            )

        db.session.add(request)
        db.session.commit()
        flash(f'Your request has been added for {client.name}!', 'success')
        return redirect(url_for('clients'))
    return render_template('requests.html', forms=form, requests_=request_list)

@app.route("/update/client/<int:client_id>", methods=['GET', 'POST'])
@login_required
def updateClient(client_id):
    form = UpdateClientForm()
    client = Clients.query.get_or_404(client_id)
    user_id = int(session['user_id'])
    if client.user_id == user_id:
        if form.validate_on_submit():
            client.name = form.name.data
            client.location = form.location.data
            db.session.add(client)
            db.session.commit()
            flash(f'{client.name} has been updated!', 'success')
            return redirect(url_for('clients'))
        elif request.method == 'GET':
            form.name.data = client.name
            form.location.data = client.location
        return render_template('update_client.html', forms=form)
    return redirect(url_for('clients'))

@app.route("/delete/client/<int:client_id>", methods=['POST'])
@login_required
def deleteClient(client_id):
    client = Clients.query.get_or_404(client_id)
    user_id = int(session['user_id'])
    if client.user_id == user_id:
        db.session.delete(client)
        client.id = None
        db.session.commit()
        flash('The client has been deleted!', 'success')
    return redirect(url_for('clients'))
    

@app.route("/update/request/<int:request_id>", methods=['GET', 'POST'])
@login_required
def updateRequest(request_id):
    form = UpdateRequestForm()
    requests = Requests.query.get_or_404(request_id)
    user_id = int(session['user_id'])
    if requests.user_id == user_id:
        if form.validate_on_submit():
            requests.title = form.title.data
            requests.description = form.description.data
            requests.target_date = form.target_date.data
            requests.product_area = form.product_area.data
            requests.client_priority = form.client_priority.data
            db.session.add(requests)
            db.session.commit()
            flash('Your request has been updated!', 'success')
            return redirect(url_for('requests', client_id=requests.client_id))
        elif request.method == 'GET':
            form.title.data = requests.title
            form.description.data = requests.description
            form.product_area.data = requests.product_area
            form.client_priority.data = requests.client_priority
        return render_template('update_req.html', forms=form)
    return redirect(url_for('requests', client_id=requests.client_id))

@app.route("/delete/request/<int:request_id>", methods=['POST'])
@login_required
def deleteRequest(request_id):
    request = Requests.query.get_or_404(request_id)
    user_id = int(session['user_id'])
    if request.user_id == user_id:
        db.session.delete(request)
        db.session.commit()
        flash('Your request has been deleted!', 'success')
    return redirect(url_for('requests', client_id=request.client_id))

@app.route("/update/<int:id>")
@login_required
def your_requests():
    client = Clients.query.filter_by(current_user.id).all()
    request = Requests.query.filter_by(current_user.id).all()
    return render_template('user.html', clients=client, requests=request)