import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from sqlalchemy import or_

from models import db, Task, User
from forms import TaskForm, TaskQuickForm, RegisterForm, LoginForm

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'login'  # redirect to login if not authenticated


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Basic config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change_this_in_prod')
    csrf.init_app(app)
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, 'tasks.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register'))
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    # Login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)

    # Logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    # Home (list + filters + quick form)
    @app.route('/')
    @login_required
    def index():
        q = request.args.get('q', '').strip()
        status = request.args.get('status', '').strip()
        sort = request.args.get('sort', 'due_date').strip()

        tasks_query = Task.query.filter_by(user_id=current_user.id)

        if q:
            like = f"%{q}%"
            tasks_query = tasks_query.filter(
                or_(Task.title.ilike(like), Task.description.ilike(like))
            )

        if status:
            tasks_query = tasks_query.filter(Task.status == status)

        if sort == 'created_at':
            tasks_query = tasks_query.order_by(Task.created_at.desc())
        elif sort == 'priority':
            tasks_query = tasks_query.order_by(Task.priority.desc(), Task.due_date.asc())
        else:
            tasks_query = tasks_query.order_by(Task.due_date.asc().nullslast())

        tasks = tasks_query.all()
        quick_form = TaskQuickForm()
        return render_template(
            'index.html',
            tasks=tasks,
            q=q,
            status=status,
            sort=sort,
            form=quick_form
        )

    # Create
    @app.route('/tasks/new', methods=['GET', 'POST'])
    @login_required
    def create_task():
        form = TaskForm()
        if form.validate_on_submit():
            task = Task(
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                status=form.status.data,
                priority=form.priority.data,
                due_date=form.due_date.data if form.due_date.data else None,
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully.', 'success')
            return redirect(url_for('index'))
        return render_template('task_form.html', form=form, heading='Create task')

    # Quick add (index inline)
    @app.route('/tasks/quick', methods=['POST'])
    @login_required
    def quick_add():
        form = TaskQuickForm()
        if form.validate_on_submit():
            task = Task(
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash('Task added.', 'success')
        else:
            flash('Title is required.', 'danger')
        return redirect(url_for('index'))

    # Edit
    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_task(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        form = TaskForm(obj=task)
        if form.validate_on_submit():
            task.title = form.title.data.strip()
            task.description = form.description.data.strip()
            task.status = form.status.data
            task.priority = form.priority.data
            task.due_date = form.due_date.data if form.due_date.data else None
            db.session.commit()
            flash('Task updated.', 'success')
            return redirect(url_for('index'))
        return render_template('task_form.html', form=form, heading='Edit task')

    # Delete
    @app.route('/tasks/<int:task_id>/delete', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'info')
        return redirect(url_for('index'))

    # Toggle status quick action
    @app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
    @login_required
    def toggle_status(task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        task.status = 'Completed' if task.status != 'Completed' else 'Pending'
        db.session.commit()
        flash('Task status updated.', 'success')
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
