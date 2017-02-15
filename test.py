
from flask import Flask
from flask import render_template
from flask import request, url_for
import logging

import MySQLdb

import dbconnect as db

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main_app():

    logging.info("attempt to connect!!")
    
    connection = db.connect_to_cloudsql()
    
    logging.info("connection successful")

    db.checkUser("Mayur", "Jain", '005892', connection)
    return "hello"


if __name__ == "__main__":
    app.run(debug=True,  port=int(8080))