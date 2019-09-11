import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()

bind = os.getenv('HOST', '0.0.0.0') + ':' + os.getenv('PORT', 5000)
