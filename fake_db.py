import random as rand
import faker as faker
from django.contrib.auth.hashers import make_password

print("\nTEACHERS\n")
names = ["Denis", "Yulia", "Sophia", "Maria", "Nikita", "Alexandr", "David", "Geo"]
surnames = ["Yakovlev", "Volkov", "Solokhin", "Nikuschenkov", "Putin", "Medvedev"]

# 1 - teacher 2 - student 3 - admin

# print("\nSTUDENTS\n")

# for i in range(10):
    # print('(2', i+10, i+10,"'" + rand.choice(names) + " " + rand.choice(surnames) + "'", "'IU7-61B'", sep=',', end='),\n')

print("\nTASKS\n")

themes = ["Mathematics", "Programming", "Literature", "Philosophy", "Biology", "Engineering"]

for i in range(100):
    print("({}, '{}.txt', '{}'),".format(i, i, rand.choice(themes)), sep='\n')
    