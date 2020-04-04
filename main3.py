import numpy as np
import random
from classes3 import User, CO2_PRICE, ELECTRICITY_PRICE, Reservoir, Bank
from collections import OrderedDict
import matplotlib
from time import time
from classes3 import produce,sell, Activity, Bank, User, Product, Needs, Loans
matplotlib.use('TkAgg')
from db_connection import init_connection
import matplotlib.pyplot as plt
import tkinter
import threading
# from microdm import find_seller, choice
from random import choice
from db_connection import insert_activity,insert_bank, insert_loan, insert_need, insert_products, insert_user
from db_connection import create_activity_table,create_bank_table,create_loan_table,create_needs_table,create_products_table,create_user_table, create_produceable_product
from db_connection import get_banks, get_banks_byuser, get_product,get_user, get_produceable_product, get_unsatisfied_need_by_product, get_user_balance
from db_connection import change_need, update_user_balance, update_loan, satisfy_need, add_user_bank


NUMBER_OF_SALES = 2
NUMBER_OF_USERS = 6
NUMBER_OF_REPEATS = 10
NAME_OF_BANKS = ["Vattenfall", "Shell"]
NAME_OF_PRODUCTS = ["bread", "eggs", "cavial"]



# def generate_dict():
#     myDict = {"bread": {"weight": 8, "price":4, "producer": True, "amount": 0.5, "energy": 0.01, "impact": 0.001},
#               "eggs": {"weight": 1.7, "price":10, "producer": False, "amount": 0.1, "energy": 0.01, "impact": 0.001},
#               "cavial": {"weight": 0.1, "price": 100, "producer": True, "amount": 0.01, "energy": 0.01, "impact": 0.001}}
#
#     return myDict
# myDict = generate_dict()


def simulation(i):


    # USER CHOOSE NEEDS OF PRODUCTS WITH RANDOM PARETIAN AMOUNT AND WEIGHT
    for user in get_user(conn):
        user_balance = user[3]
        products_result = get_product(conn)
        availability = user_balance / 2
        while (availability > 0) and len(products_result) > 0:
            chosen_product = choice(products_result)
            if user[0] is not chosen_product[2]:
                amount = random.paretovariate(3)
                weight = amount
                if (availability - (amount * weight)) >= 0:
                    availability -= amount * weight
                    insert_need(conn, user[0], chosen_product[0], chosen_product[1], amount, weight, "BUY", False)
                    products_result.remove(chosen_product)
                else:
                    break
            else:
                products_result.remove(chosen_product)
                continue


    # FOR ALL NEEDS OF BUY NOT SATISFIED, CREATE AN ACTIVITY (aka TRANSACTION - Meant as production instantiation with randomized Energy and Impact values)
    # for
    products_result = get_product(conn)
    for product_id in products_result:
        needs_to_produce = get_unsatisfied_need_by_product(conn, product_id)
        for need in needs_to_produce:
            user = need[1]
            amount = need[3]
            weight = need[4]
            energy = product_id[3] * amount
            impact = product_id[4] * amount
            producer = product_id[2]
            product = product_id[0]
            wealth = energy - impact
            incentive = energy / impact if impact > 0 else -energy / abs(impact)

            # plt.scatter(i, wealth, c='b', marker='x')
            # plt.scatter(i, energy, c='y', marker='o')
            # plt.scatter(i, impact, c='g', marker='x')

            user_balance = get_user_balance(conn, user)
            producer_balance = get_user_balance(conn, producer)[0]

            if user_balance[0] >= wealth:
                insert_activity(conn, amount, user, producer, product, energy, impact, user_balance[0], producer_balance)
                update_user_balance(conn, user, (user_balance[0] - wealth))
                satisfy_need(conn, user, product, amount, "BUY")

            else:
                print("USER DID NOT HAVE ENOUGH MONEY TO BUY")
                continue

            if energy > producer_balance:
                banks = get_banks_byuser(conn, producer)
                if banks is not None and len(banks) > 0:
                    bank = choice(banks)
                    update_loan(conn, producer, bank[0], (energy - producer_balance), energy, impact)
                    update_user_balance(conn, producer, incentive)
            else:
                update_user_balance(conn, producer, incentive + producer_balance - energy)


if __name__ == '__main__':

    conn = init_connection()

    create_user_table(conn)
    create_products_table(conn)
    create_needs_table(conn)
    create_loan_table(conn)
    create_bank_table(conn)
    create_activity_table(conn)
    create_produceable_product(conn)

    for i in range(NUMBER_OF_USERS):
        # users.append(User(100, None, None, None, None))
        insert_user(conn, 100, 0)

    for i in range(len(NAME_OF_BANKS)):
        # banks.append(Bank(NAME_OF_BANKS[i], 10000))
        insert_bank(conn)

    # HERE EACH USER CHOOSE A PRODUCT TO PRODUCE
    produceable_products = get_produceable_product(conn)
    for user in get_user(conn):
        chosen_production = choice(produceable_products) if len(produceable_products)>0 else None
        if chosen_production is not None and random.random() > 0.5:
            produceable_products.remove(chosen_production)
            insert_products(conn, chosen_production[0], chosen_production[1], chosen_production[2], user[0])
    #
    # for i in range(len(NAME_OF_PRODUCTS)):
    #     # products.append(Product(NAME_OF_PRODUCTS[i]))
    #     insert_products(conn, NAME_OF_PRODUCTS[i], myDict[NAME_OF_PRODUCTS[i]]['energy'], myDict[NAME_OF_PRODUCTS[i]]['impact'])

    # USER CHOOSE ONE RANDOM BANK
    banks = get_banks(conn)
    for user in get_user(conn):
        chosen_bank = choice(banks)
        user = user[0]; chosen_bank = chosen_bank[0]
        insert_loan(conn, chosen_bank, user, 0, 0, 0)
        add_user_bank(conn, chosen_bank, user)

    for i in range(NUMBER_OF_REPEATS):
        simulation(i)

    # a = "SELECT * FROM users join bank WHERE users.bank = bank.id AND users.id = 1"
    print("FINISHED")

    # for user in users:
    #     for product in products:
    #         availability = user.balance / 2
    #         while availability > 0:
    #             if product.name is "Bread":
    #                 needs.append(Needs(user, id(product), product.name, time(), None, 0.5, 8, "BUY" ))
    #             if product.name is "Eggs":
    #                 needs.append(Needs(user, id(product), product.name, time(), None, 0.1, 1.7, "BUY" ))
    #             if product.name is "Cavial":
    #                 needs.append(Needs(user, id(product), product.name, time(), None, 0.01, 0.1, "BUY" ))
    #
    # for user in users:
    #     user.choose_bank(banks)
    # for user in users:
    #     user.choose_need(needs)