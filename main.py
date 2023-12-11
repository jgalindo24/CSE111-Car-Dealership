import sqlite3
from sqlite3 import Error
import shutil
import os
import getpass


# openConnection(_dbFile):
_dbFile = "dealershipData.sqlite"
# print("++++++++++++++++++++++++++++++++++")
# print("Open database: ", _dbFile)

_conn = None
try:
    _conn = sqlite3.connect(_dbFile)
    # print("success")
except Error as e:
    print(e)

# print("++++++++++++++++++++++++++++++++++")

    # return conn

def closeConnection(_conn, _dbFile):
    # print("++++++++++++++++++++++++++++++++++")
    # print("Close database: ", _dbFile)

    try:
        _conn.close()
        # print("success")
    except Error as e:
        print(e)

    # print("++++++++++++++++++++++++++++++++++")


def printCentered(text):
    terminal_width = shutil.get_terminal_size().columns
    header = "{:^{width}}"
    print(header.format(text, width=terminal_width))

def inputCentered(text):
    terminal_width = shutil.get_terminal_size().columns
    header = "{:>{width}}"
    return input(header.format(text, width=(terminal_width/2)))

def vehicleView(choose):
    print("Please choose an option")
    print("1. View all")
    print("2. View filtered")
    print("3. View average miles")
    print("4. View 10 lowest priced car")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        _cur = _conn.cursor()
        _cur.execute("""
        SELECT v.v_vin, v.v_make, v.v_model, v.v_color, v.v_year, v.v_miles, v.v_price, d.d_id, d.d_name, d.d_city, d.d_state, p.p_url
        FROM vehicle v
        JOIN inventory i ON v.v_vin = i.v_vin
        JOIN dealership d ON i.d_id = d.d_id
        JOIN photo p ON v.v_vin = p.v_vin
        """)
        queryContent = _cur.fetchall()
        
        header = "{:<20} {:<10} {:<10} {:<10} {:<5} {:<10} {:<10} {:<15} {:<35} {:<25} {:<20} {:<30}"
        print((header.format("vin", "make", "model", "color", "year", "miles", "price", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')
        for vin, make, model, color, year, miles, price, d_id, d_name, d_city, d_state, p_url in queryContent:
            print((header.format(vin, make, model.split(" ")[0], color, year, miles, price, d_id, d_name, d_city, d_state, p_url[:31] + "...")) + '\n')
        print((header.format("vin", "make", "model", "color", "year", "miles", "price", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Please give filter data (if none, press [Enter] key):")
        vin = input("vin: ")
        make = input("make: ")
        model = input("model: ")
        color = input("color: ") 
        year = input("year: ")
        miles = input("miles: ")
        price = input("price: ")
        d_id = input("dealership ID: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")

        filters = {
        "v.v_vin": vin if vin.lower() != "" else None,
        "v.v_make": make if make.lower() != "" else None,
        "v.v_model": "%" + model + "%" if model.lower() != "" else None,
        "v.v_color": color if color.lower() != "" else None,
        "v.v_year": year if year.lower() != "" else None,
        "v.v_miles": miles if miles.lower() != "" else None,
        "v.v_price": price if price.lower() != "" else None,
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        }

        _cur = _conn.cursor()

        sql_query = """
            SELECT v.v_vin, v.v_make, v.v_model, v.v_color, v.v_year, v.v_miles, v.v_price, d.d_id, d.d_name, d.d_city, d.d_state, p.p_url
            FROM vehicle v
            JOIN inventory i ON v.v_vin = i.v_vin
            JOIN dealership d ON i.d_id = d.d_id
            JOIN photo p ON v.v_vin = p.v_vin
            WHERE
        """



        conditions = []
        values = []
        for key, value in filters.items():
            if value is not None:
                conditions.append(f"{key} = (?)")
                values.append(value) 

        sql_query += " AND ".join(conditions)
        # print(sql_query)

        _cur.execute(sql_query, tuple(values))
        queryContent = _cur.fetchall()
        
        header = "{:<20} {:<10} {:<10} {:<10} {:<5} {:<10} {:<10} {:<15} {:<35} {:<25} {:<20} {:<30}"
        print((header.format("vin", "make", "model", "color", "year", "miles", "price", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')
        for vin, make, model, color, year, miles, price, d_id, d_name, d_city, d_state, p_url in queryContent:
            print((header.format(vin, make, model.split(" ")[0], color, year, miles, price, d_id, d_name, d_city, d_state, p_url[:31] + "...")) + '\n')
        print((header.format("vin", "make", "model", "color", "year", "miles", "price", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')
        
        _conn.commit()
        _cur.close()
    elif choose == "3":
        print("Please give filter data (if none, press [Enter] key):")
        vin = input("vin: ")
        make = input("make: ")
        model = input("model: ")
        color = input("color: ") 
        year = input("year: ")
        miles = input("miles: ")
        d_id = input("dealership ID: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")

        filters = {
        "v.v_vin": vin if vin.lower() != "" else None,
        "v.v_make": make if make.lower() != "" else None,
        "v.v_model": "%" + model + "%" if model.lower() != "" else None,
        "v.v_color": color if color.lower() != "" else None,
        "v.v_year": year if year.lower() != "" else None,
        "v.v_miles": miles if miles.lower() != "" else None,
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        }

        _cur = _conn.cursor()

        sql_query = """
            SELECT avg(v.v_price)
            FROM vehicle v
            JOIN inventory i ON v.v_vin = i.v_vin
            JOIN dealership d ON i.d_id = d.d_id
            JOIN photo p ON v.v_vin = p.v_vin
            WHERE
        """

        conditions = []
        values = []
        var = []
        for key, value in filters.items():
            if value is not None:
                conditions.append(f"{key} = (?)")
                values.append(value)
                var.append(key)

        sql_query += " AND ".join(conditions)
        if len(var) == 0:
            sql_query = """
            SELECT avg(v.v_price)
            FROM vehicle v
            JOIN inventory i ON v.v_vin = i.v_vin
            JOIN dealership d ON i.d_id = d.d_id
            JOIN photo p ON v.v_vin = p.v_vin
            """
            _cur.execute(sql_query)
        else:
            _cur.execute(sql_query, tuple(values))    
        # print(sql_query)

        
        queryContent = _cur.fetchall()
        
        header = "{:<10}"
        # print(queryContent[0][0])
        print((header.format("avg miles")) + '\n')
        print(str(round(queryContent[0][0], 2)) + '\n')
        print(header.format("Filters:"))
        if len(var) == 0:
            print("None")
        else: 
            for i in range(len(var)):
                print(var[i].split("_")[1] + ": " + values[i])
        print()
        _conn.commit()
        _cur.close()   
    elif choose == "4":
        print("Please give filter data (if none, press [Enter] key):")
        vin = input("vin: ")
        make = input("make: ")
        model = input("model: ")
        color = input("color: ") 
        year = input("year: ")
        miles = input("miles: ")
        d_id = input("dealership ID: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")

        filters = {
        "v.v_vin": vin if vin.lower() != "" else None,
        "v.v_make": make if make.lower() != "" else None,
        "v.v_model": "%" + model + "%" if model.lower() != "" else None,
        "v.v_color": color if color.lower() != "" else None,
        "v.v_year": year if year.lower() != "" else None,
        "v.v_miles": miles if miles.lower() != "" else None,
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        }

        _cur = _conn.cursor()

        sql_query = """
            SELECT v.v_price, v.v_vin, v.v_make, v.v_model, v.v_color, v.v_year, v.v_miles, d.d_id, d.d_name, d.d_city, d.d_state, p.p_url
            FROM vehicle v
            JOIN inventory i ON v.v_vin = i.v_vin
            JOIN dealership d ON i.d_id = d.d_id
            JOIN photo p ON v.v_vin = p.v_vin
            WHERE
        """

        conditions = []
        values = []
        var = []
        for key, value in filters.items():
            if value is not None:
                conditions.append(f"{key} = (?)")
                values.append(value)
                var.append(key)

        sql_query += " AND ".join(conditions)
        if len(var) == 0:
            sql_query = """
            SELECT v.v_price, v.v_vin, v.v_make, v.v_model, v.v_color, v.v_year, v.v_miles, d.d_id, d.d_name, d.d_city, d.d_state, p.p_url
            FROM vehicle v
            JOIN inventory i ON v.v_vin = i.v_vin
            JOIN dealership d ON i.d_id = d.d_id
            JOIN photo p ON v.v_vin = p.v_vin
            """
            sql_query += "order by v.v_price asc limit 10"
            _cur.execute(sql_query)
        else:
            sql_query += "order by v.v_price asc limit 10"
            _cur.execute(sql_query, tuple(values))    
        # print(sql_query)

        
        queryContent = _cur.fetchall()
        
        header = "{:<10} {:<20} {:<10} {:<10} {:<10} {:<5} {:<10} {:<15} {:<35} {:<25} {:<20} {:<30}"
        print((header.format("avg price", "vin", "make", "model", "color", "year", "miles", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')
        for avgPrice, vin, make, model, color, year, miles, d_id, d_name, d_city, d_state, p_url in queryContent:
            print((header.format(avgPrice, vin, make, model.split(" ")[0], color, year, miles, d_id, d_name, d_city, d_state, p_url[:31] + "...")) + '\n')
        print((header.format("avg price", "vin", "make", "model", "color", "year", "miles", "dealership ID", "dealership name", "dealership city", "dealership state", "image url")) + '\n')

        _conn.commit()
        _cur.close()   



    return choose

def bookingView(choose):
    print("Please choose an option")
    print("1. View all")
    print("2. View filtered")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        _cur = _conn.cursor()
        _cur.execute("""
        SELECT b.b_id, d.d_id, d.d_name, d.d_city, d.d_state, b.b_date, b.b_time, c.c_name, e.e_name, bv.v_vin
        FROM dealership d, booking b, customer c, employee e, bookingVehicle bv
        WHERE d.d_id = b.d_id and b.c_id = c.c_id and b.e_id = e.e_id and b.b_id = bv.b_id
        """)
        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<15} {:<40} {:<25} {:<15} {:<10} {:<10} {:<20} {:<20} {:<20}"
        print((header.format("booking ID", "dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "customer", "employee", "car vin")) + '\n')
        for b_id, d_id, d_name, d_city, d_state, date, time, c_name, e_name, vin  in queryContent:
            print((header.format(b_id, d_id, d_name, d_city, d_state, date, time, c_name, e_name, vin)) + '\n')
        print((header.format("booking ID", "dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "customer", "employee", "car vin")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Please give filter data (if none, press [Enter] key):")
        d_id = input("dealership ID: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")
        date = input("date (m/d/yyyy): ")
        time = input("time: (#:## AM/PM): ")
        c_name = input("customer name: ")
        e_name = input("employee name: ")
        vin = input("vin: ")


        filters = {
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        "b.b_date": "%" + date + "%" if date.lower() != "" else None,
        "b.b_time": "%" + time + "%" if time.lower() != "" else None,
        "c.c_name": "%" + c_name + "%" if c_name.lower() != "" else None,
        "e.e_name": "%" + e_name + "%" if e_name.lower() != "" else None,
        "bv.v_vin": vin if vin.lower() != "" else None,
        }

        _cur = _conn.cursor()
        sql_query = """
        SELECT d.d_id, d.d_name, d.d_city, d.d_state, b.b_date, b.b_time, c.c_name, e.e_name, bv.v_vin
        FROM dealership d, booking b, customer c, employee e, bookingVehicle bv
        WHERE d.d_id = b.d_id and b.c_id = c.c_id and b.e_id = e.e_id and b.b_id = bv.b_id
            AND
        """

        conditions = []
        values = []
        for key, value in filters.items():
            if value is not None:
                if "%" in value:
                    conditions.append(f"{key} like (?)")
                else:
                    conditions.append(f"{key} = (?)")
                values.append(value) 

        sql_query += " AND ".join(conditions)
        # print(sql_query)

        _cur.execute(sql_query, tuple(values))
        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<40} {:<25} {:<15} {:<10} {:<10} {:<20} {:<20} {:<20}"
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "customer", "employee", "car vin")) + '\n')
        for d_id, d_name, d_city, d_state, date, time, c_name, e_name, vin  in queryContent:
            print((header.format(d_id, d_name, d_city, d_state, date, time, c_name, e_name, vin)) + '\n')
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "customer", "employee", "car vin")) + '\n')

        _conn.commit()
        _cur.close()
    return choose

def dealershipViewManager(choose):
    print("Please choose an option")
    print("1. View all")
    print("2. View filtered")
    print("3. Update Dealership Location")
    print("4. Delete a Dealership")
    print("5. Merge Dealerships")
    print("6. Delete Sold Cars")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        _cur = _conn.cursor()
        _cur.execute("""
        SELECT d.d_id, d.d_name, d.d_city, d.d_state
        FROM dealership d
        """)
        queryContent = _cur.fetchall()
        
        header = "{:<15}{:<40} {:<25} {:<15}"
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')
        for d_id, d_name, d_city, d_state in queryContent:
            print((header.format(d_id, d_name, d_city, d_state)) + '\n')
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Please give filter data (if none, press [Enter] key):")
        d_id = input("dealership id: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")


        filters = {
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        }

        _cur = _conn.cursor()
        sql_query = """
        SELECT d.d_id, d.d_name, d.d_city, d.d_state
        FROM dealership d
        WHERE 
        """

        conditions = []
        values = []
        for key, value in filters.items():
            if value is not None:
                if "%" in value:
                    conditions.append(f"{key} like (?)")
                else:
                    conditions.append(f"{key} = (?)")
                values.append(value) 

        sql_query += " AND ".join(conditions)
        # print(sql_query)

        _cur.execute(sql_query, tuple(values))
        queryContent = _cur.fetchall()
        
        header = "{:<15}{:<40} {:<25} {:<15}"
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')
        for d_id, d_name, d_city, d_state in queryContent:
            print((header.format(d_id, d_name, d_city, d_state)) + '\n')
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "3":
        print("Dealership information (Fill all out):")
        d_id = input("dealership id: ")
        d_city = input("dealership new city: ")
        d_state = input("dealership new/old state: ")

        _cur = _conn.cursor()
        sql_query = """
        UPDATE dealership 
        SET d_city = (?), d_state = (?)
        WHERE d_id = (?);
        """

        _cur.execute(sql_query, (d_city, d_state, d_id))
        
        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    elif choose == "4":
        print("Dealership information (Fill all out):")
        d_id = input("dealership id: ")

        _cur = _conn.cursor()
        _cur.execute("""
        DELETE FROM dealership WHERE d_id = (?);
        """, (d_id,))
        _cur.execute("""
        DELETE FROM inventory WHERE d_id = (?);
        """, (d_id,))
        _cur.execute("""
        DELETE FROM customerVisit WHERE d_id = (?);
        """, (d_id,))
        _cur.execute("""
        DELETE FROM employee WHERE d_id = (?);
        """, (d_id,))
        _cur.execute("""
        DELETE FROM booking WHERE d_id = (?);
        """, (d_id,))
        
        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    elif choose == "5":
        print("Parent Dealership:")
        Par_d_id = input("dealership id: ")
        print("Child Dealership:")
        Chi_d_id = input("dealership id: ")


        # filters = {
        # "d.d_id": d_id if d_id.lower() != "" else None,
        # "d.d_name": d_name if d_name.lower() != "" else None,
        # "d.d_city": d_city if d_city.lower() != "" else None,
        # "d.d_state": d_state if d_state.lower() != "" else None,
        # }

        _cur = _conn.cursor()
        _cur.execute("""
        UPDATE inventory
        SET d_id = (?)
        WHERE d_id = (?);
        """, (Par_d_id, Chi_d_id))

        _cur.execute("""
        UPDATE booking
        SET d_id = (?)
        WHERE d_id = (?);
        """, (Par_d_id, Chi_d_id))

        _cur.execute("""
        UPDATE customerVisit
        SET d_id = (?)
        WHERE d_id = (?);
        """, (Par_d_id, Chi_d_id))

        _cur.execute("""
        UPDATE employee
        SET d_id = (?)
        WHERE d_id = (?);
        """, (Par_d_id, Chi_d_id))

        _cur.execute("""
        DELETE FROM dealership
        WHERE d_id = (?);
        """, (Chi_d_id,))
        
        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    elif choose == "6":
        print("Car information (If no other car press [Enter]):")
        v_vin = input("vin: ")
        cars = []
        while v_vin != "":
            cars.append(v_vin)
            v_vin = input("vin: ")

        _cur = _conn.cursor()
        # print("""
        # DELETE FROM inventory
        # WHERE v_vin IN ({});
        # """.format(','.join(['(?)']*len(cars))))
        _cur.execute("""
        DELETE FROM inventory
        WHERE v_vin IN ({});
        """.format(','.join(['(?)']*len(cars))), tuple(cars))
        
        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    return choose

def dealershipViewCustomer(choose):
    print("Please choose an option")
    print("1. View all")
    print("2. View filtered")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        _cur = _conn.cursor()
        _cur.execute("""
        SELECT d.d_id, d.d_name, d.d_city, d.d_state
        FROM dealership d
        """)
        queryContent = _cur.fetchall()
        
        header = "{:<15}{:<40} {:<25} {:<15}"
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')
        for d_id, d_name, d_city, d_state in queryContent:
            print((header.format(d_id, d_name, d_city, d_state)) + '\n')
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Please give filter data (if none, press [Enter] key):")
        d_id = input("dealership id: ")
        d_name = input("dealership name: ")
        d_city = input("dealership city: ")
        d_state = input("dealership state: ")


        filters = {
        "d.d_id": d_id if d_id.lower() != "" else None,
        "d.d_name": d_name if d_name.lower() != "" else None,
        "d.d_city": d_city if d_city.lower() != "" else None,
        "d.d_state": d_state if d_state.lower() != "" else None,
        }

        _cur = _conn.cursor()
        sql_query = """
        SELECT d.d_id, d.d_name, d.d_city, d.d_state
        FROM dealership d
        WHERE 
        """

        conditions = []
        values = []
        for key, value in filters.items():
            if value is not None:
                if "%" in value:
                    conditions.append(f"{key} like (?)")
                else:
                    conditions.append(f"{key} = (?)")
                values.append(value) 

        sql_query += " AND ".join(conditions)
        # print(sql_query)

        _cur.execute(sql_query, tuple(values))
        queryContent = _cur.fetchall()
        
        header = "{:<15}{:<40} {:<25} {:<15}"
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')
        for d_id, d_name, d_city, d_state in queryContent:
            print((header.format(d_id, d_name, d_city, d_state)) + '\n')
        print((header.format("dealership ID", "dealership name", "dealership city", "dealership state")) + '\n')

        _conn.commit()
        _cur.close()
    return choose

def EmployeesView(choose):
    print("Please choose an option")
    print("1. View all")
    print("2. View filtered")
    print("3. Number of employees in a state")
    print("4. Employee bookings amount by month/year for a dealership")
    print("5. Fire underperforming employees from a certain year")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        _cur = _conn.cursor()
        _cur.execute("""
        SELECT e.e_id, e.e_name, e.e_email, e.e_phone, e.d_id
        FROM employee e
        """)
        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<25} {:<35} {:<15} {:<10}"
        print((header.format("employee ID", "employee name", "employee email", "employee phone", "dealership ID")) + '\n')
        for e_id, e_name, e_email, e_phone, d_id  in queryContent:
            print((header.format(e_id, e_name, e_email, e_phone, d_id)) + '\n')
        print((header.format("employee ID", "employee name", "employee email", "employee phone", "dealership ID")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Please give filter data (if none, press [Enter] key):")
        e_id = input("employee ID: ")
        e_name = input("employee name: ")
        e_email = input("employee email: ")
        e_phone = input("employee phone: ")
        d_id = input("dealership ID: ")


        filters = {
        "e.e_id": e_id if e_id.lower() != "" else None,
        "e.e_name": "%" + e_name + "%" if e_name.lower() != "" else None,
        "e.e_email": "%" + e_email + "%" if e_email.lower() != "" else None,
        "e.e_phone": e_phone if e_phone.lower() != "" else None,
        "e.d_id": d_id if d_id.lower() != "" else None,
        }

        _cur = _conn.cursor()
        sql_query = """
        SELECT e.e_id, e.e_name, e.e_email, e.e_phone, e.d_id
        FROM employee e
        WHERE
        """

        conditions = []
        values = []
        for key, value in filters.items():
            if value is not None:
                if "%" in value:
                    conditions.append(f"{key} like (?)")
                else:
                    conditions.append(f"{key} = (?)")
                values.append(value) 

        sql_query += " AND ".join(conditions)
        # print(sql_query)

        _cur.execute(sql_query, tuple(values))
        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<25} {:<35} {:<15} {:<10}"
        print((header.format("employee ID", "employee name", "employee email", "employee phone", "dealership ID")) + '\n')
        for e_id, e_name, e_email, e_phone, d_id  in queryContent:
            print((header.format(e_id, e_name, e_email, e_phone, d_id)) + '\n')
        print((header.format("employee ID", "employee name", "employee email", "employee phone", "dealership ID")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "3":
        print("City information (Fill all out):")
        d_state = input("state: ")

        _cur = _conn.cursor()
        _cur.execute("""
        SELECT COUNT(*)
        FROM employee e
        JOIN dealership d ON e.d_id = d.d_id
        WHERE d.d_state = (?);
        """, (d_state,))

        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<15}"
        print((header.format("num employees", "state")) + '\n')
        print((header.format(queryContent[0][0], d_state)) + '\n')
        print((header.format("num employees", "state")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "4":
        print("Dealership information (Fill all out):")
        d_id = input("dealership ID: ")
        print("Date information (Fill all out):")
        d_date_year = input("Year (yyyy): ")
        d_date_month = input("month (m): ")

        _cur = _conn.cursor()
        _cur.execute("""
        SELECT e.e_id, e.e_name, COUNT(*)
        FROM employee e
        JOIN booking b ON e.e_id = b.e_id
        WHERE b.d_id = (?) and strftime('%Y', b.b_date) = (?) and strftime('%m', b.b_date) = (?)
        GROUP BY e.e_id;
        """, (d_id, d_date_year, d_date_month))
        # select strftime('%Y', b.b_date) from employee e, booking b where e.e_id = b.e_id;
        queryContent = _cur.fetchall()
        
        header = "{:<15} {:<25} {:<30}"
        print((header.format("employee ID", "employee name", "Num Appointments")) + '\n')
        for e_id, e_name, countEmp in queryContent:
            print((header.format(e_id, e_name, countEmp)) + '\n')
        print((header.format("employee ID", "employee name", "Num Appointments")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "5":
        print("Dealership information (Fill all out):")
        d_id = input("dealership ID: ")
        print("Missed quota information (Fill all out):")
        amtApp = input("Fire employees who had less than this amount of appointments: ")
        d_date_year = input("During what year (yyyy): ")
        

        _cur = _conn.cursor()
        _cur.execute("""
        DELETE FROM employee
        WHERE e_id IN (
            SELECT e.e_id
            FROM employee e
            JOIN booking b ON e.e_id = b.e_id
            JOIN dealership d ON d.d_id = b.d_id
            WHERE strftime('%Y', b.b_date) = (?) AND e.d_id = (?)
            GROUP BY e.e_id
            HAVING COUNT(*) <= (?)
        );
        """, (d_date_year, d_id, amtApp))
        # select strftime('%Y', b.b_date) from employee e, booking b where e.e_id = b.e_id

        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    return choose

def appointments(choose):
    print("Please choose an option")
    print("1. View appointments")
    print("2. Book appointment")
    print("3. Delete appointment")
    print("9. Go Back")
    choose = input("Option: ")
    if choose == "1":
        print("Person Information (Fill all out)")
        c_id = input("What is your customer id: ")

        _cur = _conn.cursor()
        _cur.execute("""
        SELECT b.b_id, d.d_id, d.d_name, d.d_city, d.d_state, b.b_date, b.b_time, e.e_name, bv.v_vin
        FROM dealership d, booking b, customer c, employee e, bookingVehicle bv
        WHERE d.d_id = b.d_id and b.c_id = c.c_id and b.e_id = e.e_id and b.b_id = bv.b_id
        and b.c_id = (?)
        """, (c_id,))
        queryContent = _cur.fetchall()

        # SELECT *
        # FROM booking b
        # WHERE b.c_id = 138;
        
        header = "{:<15} {:<15} {:<40} {:<25} {:<15} {:<10} {:<10} {:<20} {:<20}"
        print((header.format("booking ID", "dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "employee", "car vin")) + '\n')
        for b_id, d_id, d_name, d_city, d_state, date, time, e_name, vin  in queryContent:
            print((header.format(b_id, d_id, d_name, d_city, d_state, date, time, e_name, vin)) + '\n')
        print((header.format("booking ID", "dealership ID", "dealership name", "dealership city", "dealership state", "date", "time", "employee", "car vin")) + '\n')

        _conn.commit()
        _cur.close()
    elif choose == "2":
        print("Person Information (Fill all out)")
        c_id = input("What is your customer id: ")
        date = input("What date(YYYY-MM-DD): ")
        time = input("What time (HH:MM AM/PM): ")
        print("Dealership information (Fill all out):")
        d_id = input("dealership ID: ")
        v_vin = input("Enter the Car's vin: ")

        _cur = _conn.cursor()
        _cur.execute("""
        INSERT INTO booking (b_date, b_time, c_id, e_id, d_id)
        VALUES ((?), (?), (?), (?), (?));
        """, (date, time, c_id, 9, d_id))

        _cur.execute("""
        select b_id from booking
        where c_id = (?)
        order by b_id desc
        limit 1;
        """, (c_id,))

        queryContent = _cur.fetchall()

        _cur.execute("""
        INSERT INTO bookingVehicle (b_id, v_vin)
        VALUES ((?), (?));
        """, (queryContent[0][0], v_vin))
        # select strftime('%Y', b.b_date) from employee e, booking b where e.e_id = b.e_id

        print("Change Complete\n")

        _conn.commit()
        _cur.close()
    elif choose == "3":
        print("Booking Information (Fill all out)")
        b_id = input("What is the booking id: ")
        

        _cur = _conn.cursor()
        _cur.execute("""
        DELETE FROM booking
        WHERE b_id = (?);
        """, (b_id,))

        _cur.execute("""
        DELETE FROM bookingVehicle 
        WHERE b_id =  (?);
        """, (b_id,))
        # select strftime('%Y', b.b_date) from employee e, booking b where e.e_id = b.e_id

        print("Change Complete\n")

        
        _cur.close()
        _conn.commit()
        # _conn.close()
        # _conn = sqlite3.connect("dealershipData.sqlite")
    return choose

def menuManager():
    while (True):
        print("Please choose an option")
        print("1. View vehicles")
        print("2. View Bookings")
        print("3. Dealerships")
        print("4. Employees")
        print("9. Exit")
        choose = input("Option: ")
        if choose == "1":
            while(True):
                choose = vehicleView(choose)
                if choose == "9":
                    break
        elif choose == "2":
            while(True):
                choose = bookingView(choose)              
                if choose == "9":
                    break
        elif choose == "3":
            while(True):
                choose = dealershipViewManager(choose)              
                if choose == "9":
                    break
        elif choose == "4":
            while(True):
                choose = EmployeesView(choose)              
                if choose == "9":
                    break
        elif choose == "9":
            break

def menuCustomer():
    while (True):
        print("Please choose an option")
        print("1. View vehicles")
        print("2. Appointments")
        print("3. Dealerships")
        print("9. Exit")
        choose = input("Option: ")
        if choose == "1":
            while(True):
                choose = vehicleView(choose)
                if choose == "9":
                    break
        elif choose == "2":
            while(True):
                choose = appointments(choose)              
                if choose == "9":
                    break
        elif choose == "3":
            while(True):
                choose = dealershipViewCustomer(choose)              
                if choose == "9":
                    break
        elif choose == "9":
            break

def login():
    os.system('clear')
    printCentered("Hello!")
    printCentered("Welcome to Dealerships.com")
    printCentered("Please Login in")
    # user = inputCentered("User: ")
    # password = inputCentered("Password: ")
    user = input("User: ")
    # password = print("Password: ", end="")
    password = getpass.getpass("Password: ")

    if user == "manager":
        print("Hello Manager")
        # DS = input("what dealership do you wish to view: ")
        menuManager()
    else:
        print("Hello " + user)
        menuCustomer()

    # print(user)

def main():
    database = r"tpch.sqlite"

    login()

    closeConnection(_conn, database)


if __name__ == '__main__':
    main()
