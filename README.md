# shipcrafter
A ship crafting system.

A simple website for creating and displaying traveller ships.

It is split into three components:  
1. A database with all the ships in it.
2. A http server to serve ships and control access to the db.
3. A website written in html and js, with some css to pretty it up.

Completed:  
Database, simple sqlite database.  
Http server, python flask server.

To Do:
1. Set up venv for the server.
2. Create the ship creation website.
3. Add the data for ship creation
4. Make some css to pretty it up.
5. Make a conversion function that converts the ship json to a markdown file.


To run in windows:  
1. Open powershell window in folder.
2. $env:FLASK_APP = "shipcrafter.py"
3. $env:FLASK_ENV="development"
3. flask run

If you want to run this in linux you don't need a guide.