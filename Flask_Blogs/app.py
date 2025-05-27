from flask import Flask, render_template, request, redirect, url_for
from models import db, BlogPost
from config import Config
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = BlogPost(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = BlogPost.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
