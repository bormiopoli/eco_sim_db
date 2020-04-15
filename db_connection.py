import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_user_table(conn):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = "DROP TABLE IF EXISTS users;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, 
        balance real unsigned CHECK (balance >= 0), wealth REAL, bank integer)"""
    try:
        cur.executescript(sql)
    except Exception as err:
        print(err)
    return cur.lastrowid


def create_needs_table(conn):
    sql = "DROP TABLE IF EXISTS needs;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS needs (id integer PRIMARY KEY AUTOINCREMENT, user integer, product integer, 
        product_name text, start_date date, end_date date, amount REAL, weight REAL, action text, satisfied BOOLEAN)"""
    cur.executescript(sql)
    return

def create_activity_table(conn):
    sql = "DROP TABLE IF EXISTS activity;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS activity (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, amount REAL,
        energy REAL, impact REAL, user integer, bank integer, seller integer, product integer, user_balance REAL, producer_balance REAL)"""
    cur.executescript(sql)
    return

def create_products_table(conn):
    sql = "DROP TABLE IF EXISTS products;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date,
        product_name text, amount REAL, producer INTEGER, produced BOOLEAN)"""
    cur.executescript(sql)

def create_produceable_product(conn):
    sql = "DROP TABLE IF EXISTS produceable_products;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS produceable_products (id integer PRIMARY KEY AUTOINCREMENT, product_name TEXT, energy REAL, impact REAL, dependency INTEGER, reservoir BOOLEAN);"""
    res = cur.execute(sql)

    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('bread', 0.01, 0.001, 4, 0);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('eggs', 0.01, 0.001, 4, 0);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('cavial', 0.1, 0.001, 6, 0);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('wheat', 0.1, 0.001, 1, 1);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('spoon', 0.1, 0.001, 7, 0);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('fish_food', 0.1, 0.001, 2, 1);"""
    cur.execute(sql)
    sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('iron', 0.1, 0.001, 3, 1);"""
    cur.execute(sql)

    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('bread', 0.01, 0.001, 4, 0);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('eggs', 0.01, 0.001, 4, 0);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('cavial', 1, 0.1, 6, 0);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('wheat', 0.01, 0.001, 1, 1);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('spoon', 10, 1, 7, 0);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('fish_food', 1, 0.1, 2, 1);"""
    # cur.execute(sql)
    # sql = """INSERT INTO produceable_products (product_name, energy, impact, dependency, reservoir) VALUES ('iron', 10, 1, 3, 1);"""
    # cur.execute(sql)

    return res.fetchall()


def create_bank_table(conn):
    sql = "DROP TABLE IF EXISTS bank;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS bank (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, amount REAL)"""
    cur.executescript(sql)
    return cur.lastrowid

def create_loan_table(conn):
    sql = "DROP TABLE IF EXISTS loans;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS loans (id integer PRIMARY KEY AUTOINCREMENT, user integer, bank integer, amount REAL, energy REAL, impact REAL)"
    cur.executescript(sql)
    return cur.lastrowid

def create_reservoir_table(conn):
    sql = "DROP TABLE IF EXISTS reservoirs;"
    cur = conn.cursor()
    cur.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS reservoirs (id integer PRIMARY KEY AUTOINCREMENT, amount REAL, energy REAL, impact REAL)"
    cur.executescript(sql)
    sql = "INSERT INTO reservoirs (amount, energy, impact) VALUES (1000, 1, 0.1)"
    cur.executescript(sql)
    sql = "INSERT INTO reservoirs (amount, energy, impact) VALUES (2000, 1, 0.1)"
    cur.executescript(sql)
    sql = "INSERT INTO reservoirs (amount, energy, impact) VALUES (3000, 1, 0.1)"
    cur.executescript(sql)
    return cur.lastrowid

def deplete_reservoir(conn, amount, reservoir_id):
    cur = conn.cursor()
    sql = "UPDATE reservoirs SET amount = amount - {0} WHERE id = {1} ;".format(amount, reservoir_id)
    cur.executescript(sql)
    return cur.lastrowid

def satisfy_need(conn, user, product, amount, action):
    sql = """UPDATE needs SET end_date = CURRENT_TIMESTAMP, satisfied = 1 
        WHERE user = {0} AND product = {1} AND amount = {2} 
        AND action like '{3}' """.format(user, product, amount, action)
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def change_need(conn, user, product, product_name, amount, weight, action):
    sql = """UPDATE needs SET amount = {3}, weight={4} WHERE user = {0} AND product = {1} 
        AND product_name like '{2}' AND action like '{5}'
        """.format(user, product, product_name, amount, weight, action)
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def update_user_balance(conn, user, balance):
    cur = conn.cursor()
    res = cur.executescript("UPDATE users SET balance = {1} WHERE id = {0}".format(user, balance))
    res = res.fetchall()
    return res

def update_loan(conn, user, bank, amount_to_add, new_energy, new_impact):
    cur = conn.cursor()
    res = cur.execute("SELECT amount, energy, impact FROM loans WHERE user = {0} AND bank = {1}".format(user, bank))
    res = res.fetchall()
    res = res[0] if res is not None and len(res)>0 else (0,0,0)
    current_loan_amount = res[0]; current_consumption = res[1]; current_impact = res[2]
    new_loan_amount = current_loan_amount + amount_to_add
    new_energy = current_consumption + new_energy
    new_impact = current_impact + new_impact
    res = cur.executescript("UPDATE loans SET amount = {0}, energy = {1}, impact = {2} WHERE bank = {3} AND user = {4};".format(new_loan_amount, new_energy, new_impact, bank, user))
    res = res.fetchall()
    return res

def add_user_bank(conn, chosen_bank, user):
    cur = conn.cursor()
    res = cur.executescript("UPDATE users SET bank = {0} WHERE id = {1};".format(chosen_bank, user))
    res = res.fetchall()
    return res

def get_banks_byuser(conn, user):
    sql = "SELECT bank FROM users WHERE id = {0}; ".format(user)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_banks(conn):
    sql = "SELECT id FROM bank; "
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_product_byname(conn, product_name):
    sql = """SELECT id, start_date, end_date,
        product_name, amount, producer, produced FROM products WHERE product_name = '{0}'; """.format(product_name)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_user(conn):
    cur = conn.cursor()
    res = cur.execute("SELECT id, start_date, end_date, balance, wealth, bank FROM users")
    res = res.fetchall()
    return res

def get_user_balance(conn, user):
    cur = conn.cursor()
    res = cur.execute("SELECT balance FROM users WHERE id = {0}".format(user))
    res = res.fetchall()
    return res[0]

def get_proddetail_byproduct(conn, product_id):
    cur = conn.cursor()
    sql = """SELECT products.id, produceable_products.energy, produceable_products.impact, dependency, reservoir
                FROM products JOIN produceable_products 
                WHERE products.product_name = produceable_products.product_name AND products.id = {0}""".format(product_id)
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_producer_by_productid(conn, product_id):
    sql = """SELECT producer 
                FROM products 
                JOIN produceable_products 
                ON produceable_products.product_name = products.product_name
                WHERE products.id = {0} ; """.format(product_id)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_product(conn):
    sql = """SELECT id, product_name, producer, produced FROM products;"""
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def get_energyimpact_by_product(conn, product_id):
    sql = """SELECT produceable_products.id, produceable_products.energy, produceable_products.impact, produceable_products.dependency, produceable_products.reservoir
                FROM products 
                JOIN produceable_products 
                ON produceable_products.product_name = products.product_name 
                WHERE products.id = {0} ;""".format(product_id)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res[0]


def get_prodname_by_dependency_id(conn, prod_id):
    sql = """SELECT id, product_name
                FROM produceable_products 
                WHERE produceable_products.id = {0} ;""".format(prod_id)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res[0]

def get_product_by_id(conn, id):
    sql = """SELECT id, product_name, producer, produced FROM products WHERE id = {0} ;""".format(id)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res[0]

def get_product_by_producer(conn, producer):
    sql = """SELECT id, product_name, producer, produced FROM products WHERE producer = {0} ;""".format(producer)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res[0]

def get_produceable_product(conn):
    sql = """SELECT product_name, energy, impact FROM produceable_products;"""
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res


def get_tot_amount_per_product(conn, product_name):
    sql = """SELECT SUM(needs.amount)
        FROM needs 
        JOIN products 
        WHERE products.id = needs.product AND needs.satisfied = 0
        AND products.product_name = '{0}' AND products.produced = 0
        GROUP BY products.id""".format(product_name)
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    if res is not None and len(res) >0:
        return res[0]
    else:
        return None

def get_unsatisfied_need_by_product(conn, product_id):
    sql = """SELECT id, user, product, amount, weight FROM needs WHERE product = {0} AND action='BUY' AND satisfied = 0;""".format(product_id[0])
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def insert_need(conn, user, product, product_name, amount, weight, action, satisfied=0):
    sql = """INSERT INTO needs (user, product, product_name, start_date, amount, weight, action, satisfied) VALUES ({0}, {1}, '{2}', CURRENT_TIMESTAMP, {3}, {4}, '{5}', {6});""".format(
        user, product, product_name, amount, weight, action, satisfied)
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def insert_user(conn, balance, wealth):
    sql = """INSERT INTO users(start_date, balance, wealth) VALUES(CURRENT_TIMESTAMP,{0},{1}); """.format(balance, wealth)
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def insert_activity(conn, amount, user, seller, prod_name, energy, impact, user_balance, producer_balance):
    cur = conn.cursor()
    sql = """INSERT INTO activity (start_date, end_date, amount, user, seller, product, energy, impact, user_balance, producer_balance) 
        VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7} );""".format(
        amount, user, seller, prod_name, energy, impact, user_balance, producer_balance)
    cur.executescript(sql)
    return cur.lastrowid

def insert_products(conn, prod_name, producer, produced=0):
    cur = conn.cursor()
    sql = """INSERT INTO products (start_date, product_name, producer, produced) VALUES (CURRENT_TIMESTAMP, '{0}', {1}, {2} );""".format(
        prod_name, producer, produced)
    cur.executescript(sql)
    return cur.lastrowid

def insert_bank(conn):
    sql = """INSERT INTO bank (start_date) VALUES (CURRENT_TIMESTAMP);"""
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def insert_loan(conn, bank, user, amount, energy, impact ):
    sql = """INSERT INTO loans (user, bank, amount, energy, impact) VALUES ({1}, {0}, {2}, {3}, {4}); """.format(bank, user, amount, energy, impact)
    cur = conn.cursor()
    cur.executescript(sql)
    return cur.lastrowid

def init_connection():
    database = r"newpythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    return conn

