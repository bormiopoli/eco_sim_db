import numpy as np
import random
from classes import User, CO2_PRICE, ELECTRICITY_PRICE, Reservoir, Bank
from collections import OrderedDict
import matplotlib
from time import time
from classes3 import produce,sell, Activity, Bank, User, Product, Needs, Loans
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter
import threading
from microdm import find_seller, choice


NUMBER_OF_SALES = 2
NUMBER_OF_USERS = 6
NUMBER_OF_REPEATS = 10
NAME_OF_BANKS = ["Vattenfall", "Shell"]
NAME_OF_PRODUCTS = ["Bread", "Eggs", "Cavial"]


def generate_dict():
    myDict = {"bread": {"weight": 8, "price":4, "producer": True, "amount": 0.5, "energy": 0.01, "impact": 0.001},
              "eggs": {"weight": 1.7, "price":10, "producer": False, "amount": 0.1, "energy": 0.01, "impact": 0.001},
              "cavial": {"weight": 0.1, "price": 100, "producer": True, "amount": 0.01, "energy": 0.01, "impact": 0.001}}

    return myDict



if __name__ == '__main__':

    users = []
    banks = []
    products = []
    needs = []

    for i in range(NUMBER_OF_USERS):
        users.append(User(100, None, None, None, None))

    for i in range(len(NAME_OF_BANKS)):
        banks.append(Bank(NAME_OF_BANKS[i], 10000))

    for i in range(len(NAME_OF_PRODUCTS)):
        products.append(Product(NAME_OF_PRODUCTS[i]))

    for user in users:
        for product in products:
            availability = user.balance / 2
            while availability > 0:
                if product.name is "Bread":
                    needs.append(Needs(user, id(product), product.name, time(), None, 0.5, 8, "BUY" ))
                if product.name is "Eggs":
                    needs.append(Needs(user, id(product), product.name, time(), None, 0.1, 1.7, "BUY" ))
                if product.name is "Cavial":
                    needs.append(Needs(user, id(product), product.name, time(), None, 0.01, 0.1, "BUY" ))

    for user in users:
        user.choose_bank(banks)
    for user in users:
        user.choose_need(needs)