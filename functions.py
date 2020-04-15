
from db_connection import get_product, get_unsatisfied_need_by_product, get_user_balance, insert_activity, insert_products, \
    update_user_balance, satisfy_need, get_banks_byuser, update_loan, deplete_reservoir, get_user, insert_need,\
    get_produceable_product, get_tot_amount_per_product, get_proddetail_byproduct, get_product_byname, get_product_by_id,\
    get_product_by_producer, get_energyimpact_by_product, get_prodname_by_dependency_id, get_producer_by_productid
from random import choice, uniform
from matplotlib import pyplot as plt
from math import log, e
from matplotlib import colors
NUMBER_OF_USERS = 7


fig = plt.figure()
colormap = None
normalize = None
plt = fig.add_subplot(111)

gain = 1

class Normalize():
    max = 0
    min = 99999999999
    id = 0

    def __init__(self, id):
        self.id = id

    @classmethod
    def standardise(cls, number):
        if number > cls.max:
            cls.max = number
        if number < cls.min:
            cls.min = number
        if cls.min == cls.max:
            return 0.5
        return (number - cls.min) / (cls.max - cls.min)

norms1 = {}
norms2 = {}
for i in range(NUMBER_OF_USERS):
    norms1[str(i+1)] = Normalize(i)
    norms2[str(i+1)] = Normalize(i)


def simulation(conn, i=0):
    # FOR ALL NEEDS OF BUY NOT SATISFIED, CREATE AN ACTIVITY (aka TRANSACTION - Meant as production instantiation with randomized Energy and Impact values)
    # for
    choose_needs(conn)
    choose_need_of_products(conn)
    choose_product_to_produce(conn)
    products_result = get_product(conn)

    for product_id in products_result:
        needs_to_produce = get_unsatisfied_need_by_product(conn, product_id)
        temp = get_energyimpact_by_product(conn, product_id[0])
        id, energy, impact, dependency, reservoir = temp if temp is not None else (None,None,None,None,None)

        for need in needs_to_produce:
            user = need[1]
            product = need[2]
            amount = need[3]
            weight = need[4]
            energy = energy * amount
            impact = impact * amount

            producer = get_producer_by_productid(conn, product_id[0])
            # ADJUST THIS PART ESPECIALLY FOR DEPLETING OF RESERVOIRS
            if (producer is not None and len(producer)>0):
                producer = producer[0][0]
            else:
                continue

            if user == producer:
                print("User IS ALSO PRODUCER")
                continue

            wealth = energy - impact
            #incentive = energy / impact if impact > 0 else -energy / abs(impact)

            user_balance = get_user_balance(conn, user)
            producer_balance = get_user_balance(conn, producer)

            # standardised_val = norms2[str(int(user))].standardise(amount)
            standardised_val = amount
            print("USER {1} Buying from {2} -> Product: {3} and Amount: {0}".format(standardised_val, user, producer, product))
            # if user == 1:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='k', marker='8')
            # if user == 2:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='b', marker='X')
            # if user == 3:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='y', marker='8')
            # if user == 4:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='g', marker='X')
            # if user == 5:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='r', marker='P')
            # if user == 6:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='m', marker='8')
            # if user == 7:
            #     plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='c', marker='X')

            satisfy_need(conn, user, product, amount, "BUY")

            if user_balance[0] >= wealth * gain:
                insert_activity(conn, amount, user, producer, product, energy, impact, user_balance[0], producer_balance[0])
                update_user_balance(conn, user, user_balance[0] - wealth * gain)
                update_user_balance(conn, producer, producer_balance[0] + wealth*gain)
            else:
                print("USER DID NOT HAVE ENOUGH MONEY TO BUY")
                continue

    for user in get_user(conn):
        user_balance = user[3]
        # standardised_val = norms1[str(int(user[0]))].standardise(user_balance)
        standardised_val = user_balance
        print(standardised_val)
        if user[0] == 1:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='k', marker='_')
        if user[0] == 2:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='b', marker='x')
        if user[0] == 3:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='y', marker='o')
        if user[0] == 4:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='g', marker='x')
        if user[0] == 5:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='r', marker='+')
        if user[0] == 6:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='m', marker='o')
        if user[0] == 7:
            plt.scatter(i, standardised_val, cmap=colormap, norm=normalize, c='c', marker='x')





def choose_needs(conn):
    products_result = get_product(conn)
    for user in get_user(conn):
        user_balance = user[3]
        availability = user_balance / 2
        i = 0

        while (availability > 0) and len(products_result) > 0 and i < 1:
            i += 1
            chosen_product = choice(products_result)
            producer = chosen_product[2]
            if user[0] is not producer:
                # amount = uniform(0, 10)
                amount = 1
                weight = 1
                if (availability - (amount * weight)) >= 0:
                    availability -= amount * weight
                    insert_need(conn, user[0], chosen_product[0], chosen_product[1], amount, weight, "BUY", False)
                    products_result.remove(chosen_product)
                    break
                else:
                    print("USER {0} CANNOT BUY ANYMORE".format(user[0]))
                    break
            else:
                pass
                #products_result.remove(chosen_product)



def choose_need_of_products(conn):
    # USER CHOOSE NEEDS OF PRODUCTS WITH RANDOM PARETIAN AMOUNT AND WEIGHT
    for user in get_user(conn):
        res = get_dependency_details(conn, user[0])
        prod_id, energy, impact, dependency, reservoir = res if res is not None else (0, 0, 0, 0, 0)
        id, prod_name = get_prodname_by_dependency_id(conn, dependency)

        if id == prod_id:
            tot_amount = get_tot_amount_per_product(conn, prod_name)

            if tot_amount is not None and len(tot_amount) > 0:
                tot_amount = tot_amount[0] if tot_amount[0] is not None else 0  # (SUPPOSING 0.6 part per unit weight are needed of dependency material)
                insert_need(conn, user[0], id, prod_name, tot_amount, 1, "BUY")
            else:
                continue

        # id, user, product, amount, weight = get_unsatisfied_need_by_product(conn, prod_id)


    # products_result = get_product(conn)
    # i=0
    # while (availability > 0) and len(products_result) > 0 and i<2:
    #     i += 1
    #     chosen_product = choice(products_result)
    #     producer = chosen_product[2]
    #     if user[0] is not producer:
    #         amount = uniform(0, 10)
    #         weight = 1
    #         if (availability - (amount * weight)) >= 0:
    #             availability -= amount * weight
    #             insert_need(conn, user[0], chosen_product[0], chosen_product[1], amount, weight, "BUY", False)
    #             products_result.remove(chosen_product)
    #         else:
    #             break
    #     else:
    #         products_result.remove(chosen_product)
    #         continue


def get_dependency_details(conn, user):

    try:
        product = get_product_by_producer(conn, user)
    except:
        product = None

    if product is not None and len(product) > 0:
        res = get_energyimpact_by_product(conn, product[0])
        prod_id = res[0]
        energy = res[1]
        impact = res[2]
        dependency = res[3]
        reservoir = res[4]
        return prod_id, energy, impact, dependency, reservoir

    else:
        return None



def choose_product_to_produce(conn):

    # HERE EACH USER CHOOSE A PRODUCT TO PRODUCE

    for user in get_user(conn):

        prod_id, energy, impact, dependency, reservoir = get_dependency_details(conn, user[0])
        try:
            product = get_product_by_producer(conn, user[0])
        except:
            product = None

        if product is not None and len(product) > 0:

            tot_amount = get_tot_amount_per_product(conn, product[1])

            if tot_amount is not None and len(tot_amount) > 0:
                tot_amount = tot_amount[0]  if tot_amount[0] is not None else 0 #(SUPPOSING 0.6 part per unit weight are needed of dependency material)

            elif tot_amount == 0:
                continue
            else:
                continue

            weight = 1

            producer = get_producer_by_productid(conn, product[0])
            producer_balance = get_user_balance(conn, producer[0][0])

            # if impact > 1:
            #     incentive =  (1/ (1 + e ** (-energy/impact)) - 0.5)
            # elif 0 < abs(impact) < 1:
            #    incentive =   (1/ (1 + e ** (-energy/abs(impact))) - 0.5)
            # elif impact == 0:
            #     incentive =  (1/ (1 + e ** (-energy)) - 0.5)
            # else:
            #     incentive =  (1/ (1 + e ** (-energy/abs(impact))) - 0.5)

            incentive = energy / impact if impact > 0 else -energy / abs(impact)

            if energy*tot_amount > producer_balance[0]:
                banks = get_banks_byuser(conn, producer[0][0])
                if banks is not None and len(banks) > 0:
                    bank = choice(banks)
                    try:
                        update_loan(conn, producer[0][0], bank[0], (energy*tot_amount - producer_balance[0]), energy*tot_amount, impact*tot_amount)
                        update_user_balance(conn, producer[0][0], incentive)
                    except:
                        pass
            else:
                update_user_balance(conn, producer[0][0], incentive + producer_balance[0])
                # THE AMOUNT OF MATERIAL NEEDED TO BE EXTRACTED FROM THE RESERVE IS VARYING UNIFORMLY AMONG 0.4 and 0.8 OF THE
                # AMOUNT NECESSARY TO CREATE A UNIT OF OUTPUT

            if reservoir == 1:
                print("USER {2} - TAKING FROM RESERVOIR NR. {0} AMOUNT: {1} ".format(dependency, str(tot_amount), user[0]))
                deplete_reservoir(conn, tot_amount, dependency)
            else:
                dependency_id, dependency_name = get_prodname_by_dependency_id(conn, dependency)
                insert_need(conn, user[0], dependency_id, dependency_name, tot_amount, weight, "BUY")


