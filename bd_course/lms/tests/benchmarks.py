import time 
import random 
from django.db import connection 
from rest_framework.test import APIClient
from django.test import TestCase
from lms.boot import TM
from lms.tests.builder import UserBuilder
from lms.serials.sers import TasksSerializer
from csv import writer
import psutil
import cProfile
import pstats

class benchmark_serialization(TestCase): 
    def setUp(self) -> None:
        self.log_file_time = writer(open('log_time.csv', "wt"))
        self.log_file_ram = writer(open("log_ram.csv", "wt"))
        self.profiler_log = open("prof_ser.txt", "wt")
        self.user_form = {'email' : '125@mail.ru', "password" : "asdasdasd", "username" : "bruh2", "grup" : "teacher"}
        self.user = UserBuilder.create_student()
        self.user.is_authenticated = True
        self.pr = cProfile.Profile()

        for i in range(1000):
            TM.create(form={"filename":f"file{i}.txt", "theme":"Maths"})

        self.data = TM.get()
        pass
    
    def test_bench(self):
        client = APIClient() 
        client.force_authenticate(user=self.user)        
        num_iterations = 100 
        
        execution_time = time.time() - time.time()
       
        for _ in range(num_iterations):  
            self.pr.enable()
            serializer = TasksSerializer(self.data, many=True)
            start_time = time.time() 
            data = serializer.data
            self.pr.disable()
            delta = time.time() - start_time
            execution_time += delta
            self.log_file_time.writerow([_, delta, psutil.cpu_percent(), serializer.data.__sizeof__() + TasksSerializer(self.data, many=True).__sizeof__()])
        
        pstats.Stats(self.pr, stream=self.profiler_log).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)
           
        self.log_file_ram.writerow(['Serializer_size', serializer.__sizeof__() + serializer.data.__sizeof__()])
 
class benchmark_data_access(TestCase):
    def setUp(self):
        self.log_file_time = writer(open('log_time_da.csv', "wt"))
        self.log_file_ram = writer(open("log_ram_da.csv", "wt"))
        self.profiler_log =  open("prof_da.txt", "wt")
    
    def test_bench(self):       
        num_iterations = 100 
        
        execution_time = time.time() - time.time()
        
        for _ in range(num_iterations):  
            start_time = time.time() 
            pr = cProfile.Profile()
            pr.enable()
            for i in range(100):
                TM.delete(filename=f'file{i}.txt')
            for i in range(100):
                TM.create(form={"filename":f"file{i}.txt", "theme":"Maths"})
            pr.disable()
            
            delta = time.time() - start_time
            execution_time += delta
            self.log_file_time.writerow([_, delta, psutil.cpu_percent(), TM.__sizeof__()+connection.__sizeof__()])
        pstats.Stats(pr, stream=self.profiler_log).sort_stats('tottime', 'cumulative', 'calls').print_stats(20)
