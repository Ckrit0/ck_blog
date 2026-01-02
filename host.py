from flask import Flask, render_template, request, redirect, url_for, jsonify
from service.store import Store

store = Store()

app = Flask(__name__)

@app.route("/")
def main():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(
    debug=True,
    host='0.0.0.0'
  )