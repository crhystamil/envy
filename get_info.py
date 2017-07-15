import twitter
import sqlite3
import time

conn = sqlite3.connect('envy.db' , check_same_thread = False)
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

def search_tw(id_tw):
    msg = 'true'
    q = api.GetUser(user_id=id_tw)
    try:
        conn.execute("UPDATE friends SET created_at =?, id_tw=?, name=?, screen_name=?, profile_image_url=?, descripcion=?, friends=?, json=?, status = 'true' WHERE id_tw = ?",(q.created_at, q.id, q.name, q.screen_name, q.profile_image_url, q.description, q.friends_count, str(q) , q.id))
        conn.commit()
        msg = "success save"
    except:
        conn.rollback()
        msg = "error in save!!!"
    
    return msg




q = conn.execute("select id_tw from friends where status = 'false'")
query = q.fetchall()

for q in query:
     print search_tw(q[0])
     time.sleep(1.5)
     print "#####################################################"




