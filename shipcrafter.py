from flask import Flask, render_templates
import random
import sqlite3
import time


app = Flask(__name__)

global conn

defaultName = "New Ship"
defaultShip = open("defaultShip.json", "r").read()

# DB Functions:

def dbFetchShipList():
	ships = conn.execute("SELECT id, name FROM ships ORDER BY timestamp")
	return ships

def dbFetchShip(id):
	return conn.execute("SELECT data FROM ships WHERE id=?", (id,)).fetchone()

def dbCreateShip():
	id = random.getrandbits(64)
	secret = random.getrandbits(64)
	timestamp = int(time.time())
	c = conn.execute(f"INSERT INTO ships VALUES ('{id}','{secret}','{timestamp}','{defaultName}','{defaultShip}')")
	c.commit()

def dbUpdateShip(id, secret, name, data):
	conn.execute("UPDATE ships set name=?, data=? WHERE id = ? AND secret = ?", (name, data, int(id), int(secret)))
	conn.commit()

# REST Functions:

@app.route('/v1/', methods=['GET'])
def webGetMainPage():
	"""Return the main site."""
	return render_template("shipcrafter.html")

@app.route('/v1/data/list.json', methods=['GET'])
def webGetShipList():
	shipList = {}
	for (id, name) in dbFetchShipList():
		shipList[id] = name
	return shipList

@app.route('/v1/data/<int:shipId>', methods=['GET'])
def webGetShipList(shipId):
	ship = dbFetchShip(shipId)
	if not ship: abort(404)
	return ship

@app.route('/v1/data/<int:shipId>/<int:shipSecret>', methods=['PUT'])
def webGetShipList(shipId, shipSecret):
	dbUpdateShip(shipId, shipSecret, request.json["name"], request.json)


# Main Check
if __name__ == "__main__":
	global conn
	conn = sqlite3.connect("shipcrafter.sqlite")
	conn.close()

