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
    sql0 = """CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, 
        balance real unsigned CHECK (balance >= 0), wealth REAL, bank integer)"""
    cur = conn.cursor()
    try:
        cur.execute(sql0)
    except Exception as err:
        print(err)
    return cur.lastrowid


def create_needs_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS needs (id integer PRIMARY KEY AUTOINCREMENT, user integer, product integer, 
        product_name text, start_date date, end_date date, amount REAL, weight REAL, action text, satisfied BOOLEAN)"""
    cur = conn.cursor()
    cur.execute(sql)
    return

def create_activity_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS activity (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, amount REAL, energy REAL, impact REAL, user integer, bank integer, seller integer, product integer)"""
    cur = conn.cursor()
    cur.execute(sql)
    return

def create_products_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, name text, amount REAL, energy REAL, impact REAL)"""
    cur = conn.cursor()
    cur.execute(sql)

# def update_products_table(conn, name, weight, amount, energy_per_material, impact_per_material):
#
#     sql = """UPDATE products SET end_date = CURRENT_TIMESTAMP, amount = REAL WHERE name like '{1}' AND id = {0} amount REAL, energy REAL, impact REAL)"""


# def create_producer_table(conn):
#     sql = """CREATE TABLE IF NOT EXISTS producers (user integer PRIMARY KEY, product integer, product_name text, start_date date, end_date date, energy REAL, impact REAL)"""
#     cur = conn.cursor()
#     cur.execute(sql)


def create_bank_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS bank (id integer PRIMARY KEY AUTOINCREMENT, start_date date, end_date date, amount REAL)"""
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def create_loan_table(conn):
    sql = "CREATE TABLE IF NOT EXISTS loans (id integer PRIMARY KEY AUTOINCREMENT, user integer, bank integer, amount REAL, energy REAL, impact REAL)"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def satisfy_need(conn, user, product, product_name, amount, weight, action):
    sql = """UPDATE needs SET end_date = CURRENT_TIMESTAMP, satisfied = TRUE 
        WHERE user = {0} AND product = {1} AND product_name like '{2}' AND amount = {3} 
        AND weight = {4} AND action like '{5}' """.format(user, product, product_name, amount, weight, action)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def change_need(conn, user, product, product_name, amount, weight, action):
    sql = """UPDATE needs SET amount = {3}, weight={4} WHERE user = {0} AND product = {1} 
        AND product_name like '{2}' AND action like '{5}'
        """.format(user, product, product_name, amount, weight, action)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def get_user(conn):
    cur = conn.cursor()
    res = cur.execute("SELECT id FROM users")
    res = res.fetchall()
    return res

def get_productionneed(conn, user):
    cur = conn.cursor()
    res = cur.execute("SELECT product, product_name FROM needs WHERE user = {0} ;".format(user[0]))
    res = res.fetchall()
    return res

def get_banks_byuser(conn, user):
    sql = "SELECT bank FROM users WHERE id = {0}; ".format(user[0])
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

def get_product(conn):
    sql = """SELECT id, name FROM products;"""
    cur = conn.cursor()
    res = cur.execute(sql)
    res = res.fetchall()
    return res

def insert_need(conn, user, product, product_name, amount, weight, action):
    sql = """INSERT INTO needs (user, product, product_name, start_date, amount, weight, action) VALUES ({0}, {1}, '{2}', CURRENT_TIMESTAMP, {3}, {4}, '{5}');""".format(
        user[0], product, product_name, amount, weight, action)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def insert_user(conn, balance, wealth):
    sql = """INSERT INTO users(start_date, balance, wealth) VALUES(CURRENT_TIMESTAMP,{0},{1}); """.format(balance, wealth)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def insert_activity(conn, amount, user, seller, bank, prod_name, energy_per_material, impact_per_material):
    cur = conn.cursor()
    sql = """INSERT INTO activity (start_date, end_date, amount, energy, impact, user, bank, seller, product) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {1}, {2}, {3}, {4}, {0}, {5}, {6});""".format(
        bank, amount, energy_per_material, impact_per_material, user, seller, prod_name)
    cur.execute(sql)
    return cur.lastrowid

def insert_products(conn, prod_name, energy_per_material, impact_per_material):
    cur = conn.cursor()
    sql = """INSERT INTO products (start_date, name, energy, impact) VALUES (CURRENT_TIMESTAMP, '{0}', {1}, {2} );""".format(
        prod_name, energy_per_material, impact_per_material)
    cur.execute(sql)
    return cur.lastrowid

def insert_bank(conn):
    sql = """INSERT INTO bank (start_date) VALUES (CURRENT_TIMESTAMP);"""
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

def insert_loan(conn, bank, user, amount, energy, impact ):
    sql = """INSERT INTO loans (user, bank, amount, energy, impact) VALUES ({1}, {0}, {2}, {3}, {4}); """.format(bank[0], user[0], amount, energy, impact)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid



def init_connection():
    database = r"newpythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    return conn

