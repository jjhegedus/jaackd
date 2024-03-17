from flask import flask
from random import randint

app = Flask(__name__)
@app.route("/<int:number>")
def get_random_number(number):
  random_number = randint(0, nmber)
  return f"Random number between 0 and {number}: {random_number}"