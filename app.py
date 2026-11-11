from flask import Flask, jsonify, request
import math

app = Flask(__name__)


@app.get('/')
def home():
    return jsonify(message='Калькулятор работает', info='/info')


@app.get('/info')
def info():
    return jsonify(description='Простой калькулятор на Flask', operations=['+', '-', '*', '/'])


@app.get('/calc/<a>/<b>')
def calculate(a, b):
    operation = request.args.get('operation', '+')
    try:
        a, b = float(a), float(b)
        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError
    except ValueError:
        return jsonify(error='Введите корректные конечные числа'), 400

    if operation == '+':
        result = a + b
    elif operation == '-':
        result = a - b
    elif operation == '*':
        result = a * b
    elif operation == '/':
        if b == 0:
            return jsonify(error='На ноль делить нельзя'), 400
        result = a / b
    else:
        return jsonify(error='Неизвестное действие'), 400
    if not math.isfinite(result):
        return jsonify(error='Результат слишком велик'), 400
    return jsonify(a=a, b=b, operation=operation, result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
