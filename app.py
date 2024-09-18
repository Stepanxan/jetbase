from flask import Flask, jsonify, request
import time
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def generate_missing_numbers(N):
    missing1 = random.randint(1, N)
    missing2 = random.randint(1, N)
    while missing1 == missing2:
        missing2 = random.randint(1, N)
    return missing1, missing2

def find_missing_numbers_sum_squares(N, missing1, missing2):
    expected_sum = N * (N + 1) // 2
    expected_sum_of_squares = N * (N + 1) * (2 * N + 1) // 6
    actual_sum = (expected_sum - missing1 - missing2)
    actual_sum_of_squares = (expected_sum_of_squares - missing1**2 - missing2**2)
    sum_missing = expected_sum - actual_sum
    sum_of_squares_missing = expected_sum_of_squares - actual_sum_of_squares
    prod_missing = (sum_missing * sum_missing - sum_of_squares_missing) // 2
    discriminant = (sum_missing * sum_missing) - 4 * prod_missing
    x = (sum_missing + int(discriminant ** 0.5)) // 2
    y = sum_missing - x
    return x, y

# def find_missing_numbers_linear(N, missing1, missing2):
#     missing = []
#     for num in range(1, N + 1):
#         if num != missing1 and num != missing2:
#             missing.append(num)
#             if len(missing) == 2:
#                 return missing
#     return missing
#
# def find_missing_numbers_xor(N, missing1, missing2):
#     xor_all = 0
#     xor_missing = 0
#     for i in range(1, N + 1):
#         xor_all ^= i
#     xor_missing = xor_all ^ missing1 ^ missing2
#     bit_flag = xor_missing & -xor_missing
#     x = 0
#     y = 0
#     for i in range(1, N + 1):
#         if i & bit_flag:
#             x ^= i
#         else:
#             y ^= i
#     if missing1 & bit_flag:
#         x ^= missing1
#     else:
#         y ^= missing1
#     if missing2 & bit_flag:
#         x ^= missing2
#     else:
#         y ^= missing2
#     return x, y

def benchmark(func, N, missing1, missing2):
    start_time = time.time()
    missing_numbers = func(N, missing1, missing2)
    end_time = time.time()
    time_taken = end_time - start_time
    return missing_numbers, time_taken

@app.route('/find-missing', methods=['POST'])
def find_missing():
    data = request.get_json()
    N = data['N']
    missing1, missing2 = generate_missing_numbers(N)

    results = {
        'missing1': missing1,
        'missing2': missing2,
        'sum_squares': benchmark(find_missing_numbers_sum_squares, N, missing1, missing2),
        # 'linear': benchmark(find_missing_numbers_linear, N, missing1, missing2),
        # 'xor': benchmark(find_missing_numbers_xor, N, missing1, missing2)
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
