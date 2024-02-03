import sys
import os
import random
from random import shuffle
seed = random.randint(1, 50)

args = sys.argv

test_files = ['solutions_tests', 'taskpacks_tests', 'userprofiles_tests', 'e2e']
random.shuffle(test_files)

for file in test_files:
    os.system(f"python3 manage.py test --shuffle {seed} lms.tests.{file}")

os.system('python3 -m pytest --alluredir=allure_results')
os.system("allure serve allure_results")