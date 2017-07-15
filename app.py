import twitter
import time
import json
import sqlite3
from json2html import *
from flask import Flask, request, render_template, redirect 

app = Flask(__name__)

conn = sqlite3.connect('envy.db' , check_same_thread = False)
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')


@app.route('/')
def main():
    query_user = "SELECT created_at, name, screen_name, descripcion, friends, id, id_tw   FROM user"
    query = conn.execute(query_user)
    users = query.fetchall()
    return render_template('index.html', users = users)

@app.route('/user/<id_user>')
def print_json(id_user):
    query_user = "select json from user where id = "+id_user
    query_user_id = "select id_tw from user where id = "+id_user
    query = conn.execute(query_user)
    query2 = conn.execute(query_user_id)
    json = query.fetchall()
    id_u = query2.fetchall()
    q_friends = "select created_at, name, screen_name, descripcion, friends, id  from friends where id_u = '"+id_u[0][0]+"'"
    query3 = conn.execute(q_friends)
    friends = query3.fetchall()
    html = json2html.convert(json =json[0][0],table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
    data = {
            'html' : html,
            'friends' : friends
            }

    return render_template('json.html', **data)

@app.route('/search')
def search():
    username =  request.args.get('q')
    if username:
        user_info = search_tw(username)
        data = {
                'user': username,
                'user_info' : user_info
               }
    else:
         data = {
                'user': username,
                'user_info' : 'Introduce un nick'
               }
    return render_template('search.html', **data)


def search_tw(user):
    msg = 'true'
    con = sqlite3.connect('envy.db')
    query_user = "SELECT created_at, name, screen_name, descripcion, friends, id   FROM user WHERE LOWER(screen_name) = '"+user.lower()+"'"
    query = con.execute(query_user)
    if not query.fetchone() :
        q = api.GetUser(screen_name=user)
        try:
            con.execute("INSERT INTO user (created_at, id_tw, name, screen_name, profile_image_url, descripcion, friends, json)  VALUES (?,?,?,?,?,?,?,?)",(q.created_at, q.id, q.name, q.screen_name, q.profile_image_url, q.description, q.friends_count, str(q) ))
            con.commit()
            msg = "success save"
        except:
            con.rollback()
            msg = "error in save!!!"
    else:
        query = con.execute(query_user)
        msg = query.fetchall()
    return msg

@app.route('/friends/<user>')
def friends(user):
    search_friends(user)
    return redirect("/")

def search_friends(user):
    query = "select id_tw from user where screen_name = '"+user+"'"
    id_us = conn.execute(query)
    id_u = id_us.fetchall()
    friends = api.GetFriendIDs(screen_name= user)
    for f in friends:
        conn.execute("INSERT INTO friends (id_tw, id_u) VALUES (?,?)",(f,id_u[0][0]))
        conn.commit()
        time.sleep(1)
    pass

@app.route('/graph/<id_tw>')
def graph(id_tw):
    q = "select id_tw, screen_name, profile_image_url from user where id_tw = '"+id_tw+"'"
    p = "select id_tw, screen_name, profile_image_url from friends where status = 'true' and id_u = '"+id_tw+"'"
    query = conn.execute(q)
    query2 = conn.execute(p)
    users = query.fetchall()
    friends = query2.fetchall()
    nodes = {
            'user' : users,
            'friends' : friends
            }
    return render_template('graph.html', **nodes)


if __name__ == '__main__':
    app.run(debug=True)

