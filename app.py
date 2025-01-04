import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# load blog posts from JSON
def load_blog_posts():
    with open("data/blog_posts.json", "r") as file:
        return json.load(file)

@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # handle form submission
        blog_posts = load_blog_posts()
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content')
        }
        blog_posts.append(new_post)

        # save the updated list to JSON file
        with open("data/blog_posts.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()

    # Remove the post with the matching ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    with open("data/blog_posts.json", "w") as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)