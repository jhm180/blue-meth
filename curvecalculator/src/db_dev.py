import psycopg2
from datetime import datetime
import os

#client = docker.from_env()
#tainers = client.containers.list()
#print(tainers)


text = str(datetime.now())
conn = psycopg2.connect(host=os.environ['DB_HOST'], port='5432', sslmode='disable', dbname='dvt-db-staging', user='pgadminuser', password='BBIgbGkD5IIDHfGx')
cur = conn.cursor()
cur.execute("INSERT INTO dvt.tester (datetime, comment) VALUES (%s, %s)", (str(datetime.now()), 'did it work?'))
conn.commit()
conn.close()
print("success")




#conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
#cur = conn.cursor()
#cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (10, 'hello@dataquest.io', 'Some Name', '123 Fake St.'))
#conn.commit()

#INSERT INTO dataset (age, name, description)
#VALUES (42, 'fred', 'desc');