# SQLite version of DB, locally hosted
import sqlite3


def model_brand_return(model, brand):
    conn = sqlite3.connect('bat_data.db')
    cur = conn.cursor()
    query = 'SELECT timestamp, amount, url FROM bat_data WHERE car_model = "{}" AND car_brand = "{}"'.format(str(model), str(brand))
    cur.execute(query)
    return cur.fetchall()


def view_brands():
    conn = sqlite3.connect('bat_data.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT car_brand FROM bat_data")
    return cur.fetchall()


def view_models(brand):
    conn = sqlite3.connect('bat_data.db')
    cur = conn.cursor()
    query = 'SELECT DISTINCT car_model FROM bat_data WHERE car_brand = "{}"'.format(str(brand))
    cur.execute(query)
    return cur.fetchall()


def active_model_in_brand(brand, model):
    conn = sqlite3.connect('bat_data.db')
    cur = conn.cursor()
    query = 'SELECT DISTINCT * FROM bat_data WHERE car_brand = "{}" AND car_model = "{}"'.format(str(brand), str(model))
    cur.execute(query)
    return cur.fetchall()


def grab_last_car_data(brand, model, ts):
    conn = sqlite3.connect('bat_data.db')
    cur = conn.cursor()
    query = 'SELECT title, title_sub, url FROM bat_data WHERE car_brand = "{}" AND car_model = "{}" AND timestamp = "{}"'.format(str(brand), str(model), str(ts))
    cur.execute(query)
    return cur.fetchall()
