from run import app
from flask import jsonify

@app.route('/')
def index():
  return jsonify({'message': 'Acá se debería ver una básica estadística del usuario.'})
