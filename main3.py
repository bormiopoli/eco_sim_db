import numpy as np
import random
from random import uniform
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
from db_connection import create_activity_table,create_bank_table,create_loan_table,create_needs_table,create_products_table,create_user_table, create_produceable_product, create_reservoir_table
from db_connection import get_banks, get_banks_byuser, get_product,get_user, get_produceable_product, \
    get_unsatisfied_need_by_product, get_user_balance, get_proddetail_byproduct, get_tot_amount_per_product, \
    get_product_byname
from db_connection import change_need, update_user_balance, update_loan, satisfy_need, add_user_bank, deplete_reservoir
from functions import simulation, choose_need_of_products, choose_product_to_produce

NUMBER_OF_USERS = 7
NUMBER_OF_REPEATS = 60
NAME_OF_BANKS = ["Vattenfall", "Shell"]

if __name__ == '__main__':

    conn = init_connection()

    create_user_table(conn)
    create_products_table(conn)
    create_needs_table(conn)
    create_loan_table(conn)
    create_bank_table(conn)
    create_activity_table(conn)
    create_produceable_product(conn)
    create_reservoir_table(conn)

    for i in range(NUMBER_OF_USERS):
        # users.append(User(100, None, None, None, None))
        insert_user(conn, 1000, 0)

    for i in range(len(NAME_OF_BANKS)):
        # banks.append(Bank(NAME_OF_BANKS[i], 10000))
        insert_bank(conn)

    # USER CHOOSE ONE RANDOM BANK
    banks = get_banks(conn)
    for user in get_user(conn):
        chosen_bank = choice(banks)
        user = user[0]; chosen_bank = chosen_bank[0]
        insert_loan(conn, chosen_bank, user, 0, 0, 0)
        add_user_bank(conn, chosen_bank, user)

    produceable = get_produceable_product(conn)
    for user in get_user(conn):
        if produceable is not None and len(produceable) > 0:
            chosen = produceable[0]
            produceable.remove(chosen)
            insert_products(conn, chosen[0], user[0], 0)

    # needs_to_produce = get_unsatisfied_need_by_product(conn, product_id)

    for i in range(NUMBER_OF_REPEATS):
        simulation(conn, i)
        plt.savefig(
            str(CO2_PRICE).replace(".", "") + "_" + str(ELECTRICITY_PRICE).replace(".", "") + "_" + str(
                NUMBER_OF_USERS) + "_" + str(NUMBER_OF_REPEATS) + ".png")


    # a = "SELECT * FROM users join bank WHERE users.bank = bank.id AND users.id = 1"
    print("FINISHED")

