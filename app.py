from numpy import poly1d

import json
import random
import re

from reedsolomon.welchberlekamp import makeEncoderDecoder
from reedsolomon.finitefield.finitefield import FiniteField
from flask import Flask, send_file, request, send_from_directory
from flask.ext.heroku import Heroku
from cStringIO import StringIO

app = Flask(__name__)
heroku = Heroku(app)

def find_next_prime(n):
    return find_prime_in_range(n, 2*n)

def find_prime_in_range(a, b):
    for p in range(a, b):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            return p
    return None

def lagrange(x, w):
    M = len(x)
    p = poly1d(0.0)
    for j in xrange(M):
        pt = poly1d(w[j])
        for k in xrange(M):
            if k == j:
                continue
            fac = x[j]-x[k]
            pt *= poly1d([1.0, -x[k]])/fac
        p += pt
    return p

class Polynomial:
    def __init__(self, coefficients = None):
        self.coefficients = coefficients if coefficients else list()

    def __str__(self):
        def variable_text(power):
            if power == 0:
                return ""
            if power == 1:
                return "x"
            return "x^" + str(power)
        description = "f(x) = "
        power = len(self.coefficients) - 1
        poly_array_representation = []
        for coefficient in self.coefficients:
            if abs(coefficient) > (10 ** -10):
                poly_array_representation.append(str(coefficient) + variable_text(power))
            power -= 1
        description = description + " + ".join(poly_array_representation)
        return description

    def evaluate(self, x):
        result = self.coefficients[-1]
        degree = len(self.coefficients) - 1
        for i in range(degree):
            power = (degree - i)
            result += (self.coefficients[i] * x ** power)
        return result

def interpolate(points):
    x_list = []
    y_list = []
    for x_p, y_p in points:
        x_list.append(x_p)
        y_list.append(y_p)
    poly = lagrange(x_list, y_list)
    return Polynomial(list(poly.coeffs))

def generate_polynomial(y_intercept, point_count):
    degree = point_count - 1
    coefficients = [random.randint(-10, 10) for _ in range(degree)]
    coefficients.append(y_intercept)
    return Polynomial(coefficients)

@app.route('/make_error_encoding')
def make_error_encoding():
    numbers_string = request.args.get('numbers', '')
    numbers = [int(element) for element in json.load(StringIO(numbers_string))]
    errors = int(request.args.get('max_errors', ''))
    total_points = len(numbers) + 2 * errors
    modulo = find_next_prime(max(numbers) + total_points + 1)

    enc, dec, solveSystem = makeEncoderDecoder(total_points, len(numbers), modulo)
    encoded = enc(numbers)
    polynomial = Polynomial(numbers)
    points = [(int(point[0]), int(point[1])) for point in encoded]
    return json.dumps({
        "polynomial": str(polynomial),
        "points": points,
        "modulo": modulo
    })

@app.route('/find_error_encoding')
def find_error_encoding():
    points_string = request.args.get('points', '')
    points = json.load(StringIO(points_string))
    total_points = len(points)
    length = int(request.args.get('length', ''))
    modulo = int(request.args.get('modulo', ''))
    Fp = FiniteField(modulo)
    enc, dec, solveSystem = makeEncoderDecoder(total_points, length, modulo)
    Q,E = solveSystem([[Fp(point[0]), Fp(point[1])] for point in points])
    P, remainder = (Q.__divmod__(E))
    polynomial = Polynomial([int(coefficient) for coefficient in P.coefficients])
    return json.dumps({
        "polynomial": str(polynomial),
        "coefficients": polynomial.coefficients
    })

@app.route('/make_secret')
def make_secret():
    secret = int(request.args.get('secret', ''))
    total_points = int(request.args.get('total_points', ''))
    required_points = int(request.args.get('required_points', ''))
    polynomial = generate_polynomial(secret, required_points)

    points = []
    for i in range(1, total_points + 1):
        points.append((i, polynomial.evaluate(i)))
    return json.dumps({
        "polynomial": str(polynomial),
        "points": points
    })

@app.route('/find_secret')
def find_secret():
    points_string = request.args.get('points', '')
    points = json.load(StringIO(points_string))
    polynomial = interpolate(points)
    return json.dumps({
        "polynomial": str(polynomial),
        "secret": polynomial.evaluate(0)
    })

@app.route('/plot')
def plot():
    image = StringIO()
    points_string = request.args.get('points', '')
    points = json.load(StringIO(points_string))
    interpolate(points, image)
    image.seek(0)
    return send_file(image, attachment_filename="image.png", as_attachment=False)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/html/<path:path>')
def send_html(path):
    return send_from_directory('static/html', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/')
@app.errorhandler(404)
def index(*args):
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
