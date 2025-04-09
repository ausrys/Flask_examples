from flask import Flask
app = Flask(__name__)

cache: dict = {}


def recur_fibo(n: int) -> int:

    # Check if the value is already cached
    if n in cache:
        return cache[n]

    if n <= 1:
        return n
    # Compute and cache the Fibonacci value
    result = recur_fibo(n - 1) + recur_fibo(n - 2)
    cache[n] = result
    return cache[n]


@app.route('/simple/<int:num>', methods=['GET'])
def fibo(num):
    result = {
        "user_input": num,
        "Fibo_result": recur_fibo(num)
    }
    return result


@app.route('/odd/<int:num>', methods=['GET'])
def is_odd(num):
    is_odd_in_sequence = "Not in sequence" if (
        recur_fibo(num)) % 2 == 0 else "In sequence"
    result = {
        "user_input": num,
        "result": is_odd_in_sequence,
        "fibo_number": recur_fibo(num)
    }
    return result


if __name__ == '__main__':
    app.run(debug=True)
