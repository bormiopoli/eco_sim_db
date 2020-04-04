

myDict = {"bread": {"weight": 8, "price":4, "producer": True, "amount": 0.5, "energy": 0.01, "impact": 0.001}, "eggs":{"weight": 1.7, "price":10, "amount": 0.1,  "producer": True, "energy": 0.01, "impact": 0.001}, "cavial": {"weight":0.1, "price": 100,  "producer": True, "amount": 0.01, "energy": 0.01, "impact": 0.001}}


def choice(myDict):
    # maxdict = max(myDict, key=myDict.get)
    prod_names = sorted(myDict, key=lambda x: myDict[x]["weight"], reverse=True)
    for prod_name in prod_names:
        price = myDict.get(prod_name)['price']
        amount = myDict.get(prod_name)['amount']
        energy = myDict.get(prod_name)['energy']
        impact = myDict.get(prod_name)['impact']
        del myDict[str(prod_name)]
        yield prod_name, amount, price, energy, impact

# REDEFINE THE FIND SELLER AS API WITH DICT FOR UPDATING RESOURCE, ACTIVITIES AND PRODUCTS
def find_seller(users, prod_name, amount, price):
    for user in users:
        if user.production.get(prod_name) is not None and user.production[str(prod_name)]["producer"] == True:
            if amount <= user.stock:
                return user
            else:
                print("User {0} did not have enough money to buy {2} Kg of {1}".format(user.id, prod_name, amount))
    return None

def bargain(buyer, sender):
    pass





