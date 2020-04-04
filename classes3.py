from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import random
from random import choice
import math
import logging
from time import time

DEPTH = 6

import math
# class Country:
import threading
#     name = country_list.

ELECTRICITY_PRICE = 0.80 # E / kWh
CO2_PRICE = 28 # E/ton
CLEANNESS = 0.0005  # must be muliplied by a random number (after) units: tonCO2eq./kWh  0.0005 stands for average of 500gCO2eq./kWh


class User:

    def __init__(self, balance, production, need, wealth, bank):
        self.id = id(self)
        self.balance = balance
        self.production = production
        self.need = need
        self.wealth = wealth
        self.bank = bank

    def choose_bank(self, banks):
        chosen = choice(banks)
        self.need = chosen.id
        banks = banks.remove(chosen)
        return banks

    def choose_need(self, needs):
        chosen = choice(needs)
        self.need = chosen.id
        needs = needs.remove(chosen)
        return needs


class Bank:

    def __init__(self, name, balance):
        self.id = id(self)
        self.name = name
        self.balance = balance
        self.total_lend = 0


class Reservoir:

    value = None

    def __init__(self, amount, extraction_price=None):
        self.country = "Italy"
        self.id = id(self)
        self.amount = amount
        self.price = 3 # $/unit
        self.update(self.price, self.amount)

    @classmethod
    def update(cls, price, amount):
        cls.value = price * amount


class Product:

    def __init__(self, name):
        self.id = id(self)
        self.name = name
        self.energy_per_material = 1 / (random.random() * random.random())
        self.impact_per_material = 100 / (random.random() * random.random())


class Activity:

    def __init__(self, amount, energy, impact, user, bank, seller, product):
        self.id = id(self)
        self.amount = amount
        self.energy = energy
        self.impact = impact
        self.user   = user
        self.bank   = bank
        self.seller = seller
        self.product= product


class Needs:

    def __init__(self, user, product, product_name, start_date, end_date, amount, weight, action):
        self.id = id(self)
        self.user = user
        self.product = product
        self.product_name = product_name
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount
        self.weight = weight
        self.action = action
        self.satisfied = False


class Loans:

    def __init__(self, user, bank, amount, energy, impact, start_date, end_date):
        self.id = id(self)
        self.user = user
        self.bank = bank
        self.amount = amount
        self.energy = energy
        self.impact = impact
        self.start_date = start_date
        self.end_date = end_date


def sell(seller, buyer, amount, bank, price):

    # for seller in self.dependencies:
    if buyer.balance >= amount * price:
        buyer.balance -= amount
    elif buyer.wealth >= amount:
        buyer.wealth -= amount
    else:
        lend = bank.loan(amount)
        seller.wealth += lend
        print("User {0} borrowed loan of [ {2} ] from bank to pay to {1}".format(buyer.id, seller.id, amount))

    if seller.wealth >= seller.balance:
        seller.balance += amount  # users sell at a random increased price from the objective value it has spent for its production
    else:
        seller.wealth += amount

    buyer.wealth += amount
    seller.wealth -= amount
    print("Buyer {0} bought from seller {1}".format(buyer.id, seller.id))
    # if rec < DEPTH:
    #     buyer.produce(amount, bank, rec)
    # else:
    #     logging.info("**** DID NOT HAVE MONEY TO BUY")
    #     pass



# amount is assumed to be exactly the energy required to produce it minus its impacts
def produce(productor, amount, bank, rec, energy_per_material, impact_per_material):

    if (amount * energy_per_material * ELECTRICITY_PRICE) < productor.balance or (amount * energy_per_material * ELECTRICITY_PRICE) < productor.wealth:
        productor.stock += amount
        productor.consumption = energy_per_material * amount
        productor.tot_consumption += productor.consumption
        productor.impact = impact_per_material * amount
        productor.tot_impact += productor.impact

        if productor.balance < productor.consumption * ELECTRICITY_PRICE:
            productor.wealth -= productor.consumption * ELECTRICITY_PRICE
        else:
            productor.balance -= productor.consumption * ELECTRICITY_PRICE
        prod_wealth = productor.consumption * ELECTRICITY_PRICE - productor.impact * CO2_PRICE
        productor.wealth += prod_wealth
        lend = bank.lend(productor.consumption * ELECTRICITY_PRICE, productor.impact*CO2_PRICE)
        print("User {0} has produced buying from energy bank {1}".format(productor.id, bank.id))
        # self.balance += lend REMOVED USER IS COMPENSATED IN OTHER CURRENCY RELATIVE TO WEALTH
        plt.scatter(rec, productor.consumption, c='b', marker='x', label='1')
        plt.scatter(rec, productor.wealth, c='y', marker='x', label='3')
        plt.scatter(rec, productor.balance, c='g', marker='o', label='0')
        plt.scatter(rec, productor.impact, c='r', marker='s', label='2')
        plt.scatter(rec, (productor.balance - productor.wealth), c='m', marker='o', label='4')

    else:
        prod_wealth = 0
        # lend = bank.lend(amount=(amount * self.energy_per_material * ELECTRICITY_PRICE), impact=self.impact)
        # self.wealth += amount * self.energy_per_material * ELECTRICITY_PRICE
        print("User {0} could not buy because did not have enough money for pay electricity {1}".format(productor.id,
                                                                                                        productor.energy_per_material * amount * ELECTRICITY_PRICE))
    return prod_wealth


