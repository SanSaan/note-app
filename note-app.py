from flask import Flask, abort, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def get_all_posts():
    log('Get all posts')
    posts = query_db("SELECT * FROM posts")
    return posts

@app.route('/posts/<int:post_id>', methods = ['GET', 'POST', 'DELETE'])
def post(post_id):
    if request.method == 'GET':
        log('Get post by ' + str(post_id))
        post = get_post(post_id)
        return jsonify(post)

    if request.method == 'POST':
        log('Create post')
        data = request.get_json()
        insert_query_db('INSERT INTO posts (title, content) VALUES (?, ?)',
            (data['title'], data['content'])
            )
        return '', 200

    if request.method == 'DELETE':
        log('Delete post')
        insert_query_db('DELETE FROM posts WHERE id = ?', (post_id,))
        return '', 200


@app.route('/history')
def history_by_search():
    search = request.args.get('search')
    with open('logs.txt') as f:
        text = f.read().split('\n')
        if search:
            return [line for line in text if search in line]
        else:
            return text

def get_post(post_id):
    post = query_db('SELECT * FROM posts WHERE id = ?', (post_id,), True)
    if post is None:
        abort(404)
    return post

def query_db(query, args=(), one=False):
    cur = get_db_connection().execute(query, args)
    if one:
        rv = cur.fetchone()
    else:
        rv = cur.fetchall()
    cur.close()
    return rv

def insert_query_db(query, args):
    conn = get_db_connection()
    cur = conn.execute(query, args)
    conn.commit()
    cur.close()

def get_db_connection():
    return sqlite3.connect('database.db')

def log(message: str):
    with open('logs.txt', 'a') as f:
        f.write(message + '\n')
    app.logger.info(message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)