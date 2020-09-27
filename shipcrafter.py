from flask import Flask, jsonify, request, send_from_directory
import json
import random
import sqlite3
import time

app = Flask(__name__, static_url_path='')
app.config['JSON_SORT_KEYS'] = False

# ship class
class Ship:
	def __init__(self, id, secret, timestamp, name, data):
		self.id = id
		self.secret = secret
		self.timestamp = timestamp
		self.name = name
		self.data = data
		

# DB Functions:
def dbGetConnection():
	return sqlite3.connect("shipcrafter.sqlite")

def dbCreateTable():
	dbEnsureConnection()
	conn.execute("""
CREATE TABLE IF NOT EXISTS 'ships'
(
	'id'	INTEGER NOT NULL UNIQUE,
	'secret'	INTEGER NOT NULL,
	'timestamp'	INTEGER NOT NULL,
	'name'	TEXT,
	'data'	TEXT,
	PRIMARY KEY('id')
)
""")
	conn.commit()

def dbFetchShipList():
	connection = dbGetConnection()
	ships = connection.execute("SELECT id, name, timestamp FROM ships ORDER BY timestamp DESC")
	shipList = []
	for (id, name, timestamp) in ships:
		shipList.append(Ship(id, None, timestamp, name, None))
	connection.close()
	return shipList

def dbFetchShip(id):
	connection = dbGetConnection()
	result = connection.execute("SELECT data FROM ships WHERE id=?", (id,)).fetchone()
	connection.close()
	if result is not None:
		(ship,) = result
		return ship
	else:
		return """{name" = "404"}"""

def dbCreateShip(id):
	connection = dbGetConnection()
	defaultName = "New Ship"
	defaultShip = open("defaultShip.json", "r").read()
	if id != 0:
		oldShip = json.loads(dbFetchShip(id))
		oldShip["name"] = "Clone of " + oldShip["name"]
		defaultShip = json.dumps(oldShip)
		defaultName = oldShip["name"]
	id = random.getrandbits(63)
	secret = random.getrandbits(63)
	timestamp = int(time.time())
	connection.execute("INSERT INTO ships (id, secret, timestamp, name, data) VALUES (?, ?, ?, ?, ?)", (id, secret, timestamp, defaultName, defaultShip))
	connection.commit()
	connection.close()
	return (id, secret)

def dbUpdateShip(id, secret, name, data):
	connection = dbGetConnection()
	timestamp = int(time.time())
	connection.execute("UPDATE ships set timestamp=?, name=?, data=? WHERE id = ? AND secret = ?", (timestamp, str(name), str(data), int(id), int(secret)))
	connection.commit()
	connection.close()

# REST Functions:

@app.route('/v1/', methods=['GET'])
def webGetMainPage():
	"""Return the main site."""
	return send_from_directory(".", "shipcrafter.html")

@app.route('/v1/shipcrafter.js', methods=['GET'])
def webGetJs():
	"""Return the main site."""
	return send_from_directory(".", "shipcrafter.js")

@app.route('/v1/data/list.json', methods=['GET'])
def webGetShipList():
	return jsonify(dbFetchShipList())

@app.route('/v1/data/<int:shipId>', methods=['GET'])
def webGetShip(shipId):
	ship = dbFetchShip(shipId)
	return jsonify(json.loads(ship))

@app.route('/v1/data/<int:shipId>/<int:shipSecret>', methods=['PUT'])
def webUpdateShip(shipId, shipSecret):
	dbUpdateShip(shipId, shipSecret, request.json["name"], json.dumps(request.json))
	ship = dbFetchShip(shipId)
	return jsonify(json.loads(ship))

@app.route('/v1/data/newship', methods=['GET'])
def webCreateNewShip():
	(id, secret) = dbCreateShip(0)
	ship = dbFetchShip(id)
	return jsonify(json.loads(ship))

@app.route('/v1/data/newship/<int:shipId>', methods=['GET'])
def webClonehip(shipId):
	(id, secret) = dbCreateShip(shipId)
	ship = dbFetchShip(id)
	return jsonify(json.loads(ship))

# Main Check
if __name__ == "__main__":
	global conn
	conn = sqlite3.connect("shipcrafter.sqlite")
	dbCreateTable()
	
	conn.close()

