import os
import secrets

from flask import render_template, url_for, flash, redirect, request
from Mybook import app, db, bcrypt
from Mybook.models import User,Post
from Mybook.forms import RegistrationForm,LoginForm,PostForm
from flask_login import login_user, current_user, logout_user, login_required

 
@app.route("/")


@app.route("/home",methods=['GET', 'POST'])
@login_required
def home():
  
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("index.html", posts=posts)

@app.route("/landing",methods=['GET', 'POST'])
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()


    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            ##login_user(user)
            ##redirect(url_for('home'))
            flash(f'Login Unsuccessful. Please check username and password', 'danger')

    return render_template("landing.html", form=form)

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('landing'))
    return render_template("signup.html",form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/posts', picture_fn)
    form_picture.save(picture_path)
    return picture_fn



@app.route("/post",methods=['GET', 'POST'])
@login_required
def post():
    form=PostForm()
    if form.validate_on_submit():
        
        picture_file = save_picture(form.picture.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user,image_file=picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing')) 


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('profile'))

@app.route("/profile",methods=['GET', 'POST'])
@login_required
def profile():
    #posts = Post.query.all()
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc())
    #posts = User.query.filter_by(title == current_user)
    return render_template("profile.html", posts=posts)