from django.core.management.base import BaseCommand
from site1.models import Plorts
import re

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file1 = []
        with open('C:\\Users\\Foxy\\PycharmProjects\\GraduarionProject\\graduarion_project\\site1\\utils\\plorts.txt',
                  'r', encoding='UTF-8') as f:
            for i in f.read().split('/n'):
                file1.append(i)
        list1 = []
        for i in file1:
            for j in range(0, 17):
                list2 = []
                list2.append(re.findall(r'([A-Z][a-z]+\s+[A-Z][a-z]+)[|]', i)[j])
                list2.append(re.findall(r'[|](.+)[(]', i)[j])
                list2.append(re.findall(r'[(](.+)[)]', i)[j])
                list2.append(re.findall(r'[)](.+[.!]+)', i)[j])
                list2.append(re.findall(r'[.!](\d{1,3}\b)', i)[j])
                list1.append(list2)
        for i in list1:
            Plorts(plortName=i[0], imagePlort=i[1], rarity=i[2], description=i[3], price=i[4], quantity=1000).save()
