from flask import Flask, render_template, url_for, flash, redirect
from requests import app, db, bcrypt
from requests.forms import LoginForm, ClientForm, RequestForm
from requests.models import User, Requests, Clients
from flask_login import login_user, login_required


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'Welcome {user.username}, you are logged in!', 'success')
            return redirect(url_for('clients'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', forms=form)


@app.route("/clients", methods=['GET', 'POST'])
def clients():
    form = ClientForm()
    client_list =Clients.query.all()
    if form.validate_on_submit():
        client = Clients(name=form.name.data, location=form.location.data)
        db.session.add(client)
        db.session.commit()
        flash(f'{client.name} has been added!', 'success')
        return redirect(url_for('clients'))
    return render_template('clients.html', forms=form, clients=client_list, title='Clients')


@app.route("/clients/<int:client_id>")
def requests(client_id):
    form = RequestForm()
    #  requests=client_requests, add this when done with the form
    return render_template('requests.html', forms=form, title='Feature Requests')


@app.route("/your-requests")
def your_requests():
    return "Your requests"

