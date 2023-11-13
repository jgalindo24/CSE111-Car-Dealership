import sqlite3
from sqlite3 import Error
import random
import uuid


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")

    _cur = _conn.cursor()

    dealershipCreate = """
    create table if not exists dealership (
        d_id integer primary key,
        d_name char(100) not null,
        d_city char(100) not null,
        d_state char(100) not null
    );
    """
    _cur.execute(dealershipCreate)
    _conn.commit()

    inventoryCreate = """ 
    create table if not exists inventory (
        v_vin char(100) not null,
        i_dateOfArrival date not null,
        d_id integer not null
    );
    """
    _cur.execute(inventoryCreate)
    _conn.commit()

    vehicleCreate = """
    create table if not exists vehicle (
        v_vin char(100) primary key,
        v_make char(100) not null,
        v_model char(100) not null,
        v_color char(100) not null,
        v_year decimal(4,0) not null,
        v_miles decimal(10,0) not null,
        v_price decimal(10,0) not null,
        v_titleStatus char(100) not null,
        v_bodyStyle char(100) not null
    );
    """
    _cur.execute(vehicleCreate)
    _conn.commit()
    
    photoCreate = """
    create table if not exists photo (
        p_url char(100) primary key,
        v_vin integer not null
    );
    """
    _cur.execute(photoCreate)
    _conn.commit()

    employeeCreate = """
    create table if not exists employee (
        e_id integer primary key,
        e_name char(100) not null,
        e_email char(100) not null,
        e_phone char(100) not null,
        d_id integer not null references dealership(d_id) on delete cascade
    );
    """
    _cur.execute(employeeCreate)
    _conn.commit()
    
    customerCreate = """
    create table if not exists customer (
        c_id integer primary key,
        c_name char(100) not null,
        c_email char(100) not null,
        c_phone char(100) not null
    );
    """
    _cur.execute(customerCreate)
    _conn.commit()
    
    customerVisitCreate = """
    create table if not exists customerVisit (
        d_id integer not null,
        c_id integer not null
    );
    """
    _cur.execute(customerVisitCreate)
    _conn.commit()
    
    bookingCreate = """
    create table if not exists booking (
        b_id integer primary key,
        b_date date not null,
        b_time time not null,
        c_id integer not null,
        e_id integer not null,
        d_id integer not null
    );
    """
    _cur.execute(bookingCreate)
    _conn.commit()
    
    bookingVehicle = """
    create table if not exists bookingVehicle (
        b_id integer not null,
        v_vin integer not null
    );
    """
    _cur.execute(bookingVehicle)
    _conn.commit()

    _cur.close()

    print("++++++++++++++++++++++++++++++++++")


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")

    _cur = _conn.cursor()

    dealershipDrop = """
    drop table if exists dealership;
    """
    _cur.execute(dealershipDrop)
    _conn.commit()

    inventoryDrop = """
    drop table if exists inventory;
    """
    _cur.execute(inventoryDrop)
    _conn.commit()

    vehicleDrop = """
    drop table if exists vehicle;
    """
    _cur.execute(vehicleDrop)
    _conn.commit()

    photoDrop = """
    drop table if exists photo;
    """
    _cur.execute(photoDrop)
    _conn.commit()

    employeeDrop = """
    drop table if exists employee;
    """
    _cur.execute(employeeDrop)
    _conn.commit()

    customerDrop = """
    drop table if exists customer;
    """
    _cur.execute(customerDrop)
    _conn.commit()

    customerVisitDrop = """
    drop table if exists customerVisit;
    """
    _cur.execute(customerVisitDrop)
    _conn.commit()

    bookingDrop = """
    drop table if exists booking;
    """
    _cur.execute(bookingDrop)
    _conn.commit()

    bookingVehicleDrop = """
    drop table if exists bookingVehicle;
    """
    _cur.execute(bookingVehicleDrop)
    _conn.commit()

    # _cur.execute(sqlQuery)
    # _conn.commit()

    _cur.close()

    print("++++++++++++++++++++++++++++++++++")


def populateTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table")

    _cur = _conn.cursor()



    # vehicle Table Population
    vehicleFile = open("vehicles.csv")
    vehicleData = vehicleFile.readlines()
    vehicleFile.close()

    for i in range(0, len(vehicleData)):
        vehicleData[i] = vehicleData[i].strip()
        vehicleData[i] = vehicleData[i].split(",")
    
    # print(vehicleData[0])
    for i in range(1, len(vehicleData)):
        sqlQuery = """
        insert into vehicle (v_vin, v_make, v_model, v_color, v_year, v_miles, v_price, v_titleStatus, v_bodyStyle) values (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        _cur.execute(sqlQuery, (vehicleData[i][7], vehicleData[i][3], vehicleData[i][4], vehicleData[i][9], int(vehicleData[i][2]), int(vehicleData[i][5]), int(vehicleData[i][1]), vehicleData[i][6], vehicleData[i][8]))
        # print(s_name)
    _conn.commit()



    # photo Table Population

    base_url='https://dealership.com/image/'
    extension='.jpg'
    imageURLs = []
    for i in range(1, len(vehicleData)):
        unique_id = str(uuid.uuid4())
        imageURLs.append(f"{base_url}{unique_id}{extension}")

    for i in range(1, len(vehicleData)):
        sqlQuery = """
        insert into photo (p_url, v_vin) values (?, ?);
        """
        _cur.execute(sqlQuery, (imageURLs[i - 1], vehicleData[i][7]))
    _conn.commit()



    # dealership Table Population
    DNFile = open("dealershipNames.csv")
    DNData = DNFile.readlines()
    DNFile.close()
    for i in range(0, len(DNData)):
        DNData[i] = DNData[i].strip()

    CSFile = open("city&States.csv")
    CSData = CSFile.readlines()
    CSFile.close()
    for i in range(0, len(CSData)):
        CSData[i] = CSData[i].strip()
        CSData[i] = CSData[i].split(",")
    uniqueIndexes = random.sample(range(1, 1001), 100)
    # print(uniqueIndexes)
    
    for i in range(1, 101):
        sqlQuery = """
        insert into dealership (d_name, d_city, d_state) values (?, ?, ?);
        """
        _cur.execute(sqlQuery, (DNData[i], CSData[uniqueIndexes[i-1]][0], CSData[uniqueIndexes[i-1]][1]))
    _conn.commit()


    
    # inventory Table Population
    DOAFile = open("dates&Time.csv")
    DOAData = DOAFile.readlines()
    DOAFile.close()
    for i in range(0, len(DOAData)):
        DOAData[i] = DOAData[i].strip()
        DOAData[i] = DOAData[i].split(",")
    
    _cur.execute("""
    select v_vin from vehicle
    """)
    vins = _cur.fetchall()

    _cur.execute("""
    select d_id from dealership
    """)
    dealershipIDs = _cur.fetchall()
    # print(vins[0][0])

    for i in range(len(vins)):
        sqlQuery = """
        insert into inventory (v_vin, i_dateOfArrival, d_id) values (?, ?, ?);
        """
        _cur.execute(sqlQuery, (vins[i][0], DOAData[random.randint(1, 1000)][0], dealershipIDs[random.randint(0, 99)][0]))
    _conn.commit()



    # employee Table Population
    CIEFile = open("contactInfoEmployees.csv")
    CIEData = CIEFile.readlines()
    CIEFile.close()
    for i in range(0, len(CIEData)):
        CIEData[i] = CIEData[i].strip()
        CIEData[i] = CIEData[i].split(",")
    
    uniqueIndexes = random.sample(range(1, 1001), 1000)

    for i in range(1000):
        sqlQuery = """
        insert into employee (e_name, e_email, e_phone, d_id) values (?, ?, ?, ?);
        """
        _cur.execute(sqlQuery, (CIEData[uniqueIndexes[i]][0], CIEData[uniqueIndexes[i]][1], CIEData[uniqueIndexes[i]][2], dealershipIDs[random.randint(0, 99)][0]))
    _conn.commit()

    # customer Table Population
    CICFile = open("contactInfoCustomers.csv")
    CICData = CICFile.readlines()
    CICFile.close()
    for i in range(0, len(CICData)):
        CICData[i] = CICData[i].strip()
        CICData[i] = CICData[i].split(",")
    
    uniqueIndexes = random.sample(range(1, 1001), 1000)

    for i in range(1000):
        sqlQuery = """
        insert into customer (c_name, c_email, c_phone) values (?, ?, ?);
        """
        _cur.execute(sqlQuery, (CICData[uniqueIndexes[i]][0],CICData[uniqueIndexes[i]][1], CICData[uniqueIndexes[i]][2]))
    _conn.commit()



    # customerVisit Table Population    
    _cur.execute("""
    select c_id from customer
    """)
    customerIDs = _cur.fetchall()

    for i in range(3000):
        sqlQuery = """
        insert into customerVisit (d_id, c_id) values (?, ?);
        """
        _cur.execute(sqlQuery, (dealershipIDs[random.randint(0, 99)][0], customerIDs[random.randint(0, 999)][0]))
    _conn.commit()



    # booking Table Population
    _cur.execute("""
    select e_id from employee
    """)
    employeeIDs = _cur.fetchall()

    for i in range(2000):
        sqlQuery = """
        insert into booking (b_date, b_time, c_id, e_id, d_id) values (?, ?, ?, ?, ?);
        """
        _cur.execute(sqlQuery, (DOAData[random.randint(1, 1000)][0], DOAData[random.randint(1, 1000)][1], customerIDs[random.randint(0, 999)][0], employeeIDs[random.randint(0, 999)][0], dealershipIDs[random.randint(0, 99)][0]))
    _conn.commit()



    # bookingVehicles Table Population
    _cur.execute("""
    select b_id from booking
    """)
    bookingIDs = _cur.fetchall()

    for i in range(4000):
        sqlQuery = """
        insert into bookingVehicle (b_id, v_vin) values (?, ?);
        """
        _cur.execute(sqlQuery, (bookingIDs[random.randint(0, 1999)][0], vins[random.randint(0, len(vins)-1)][0]))
    _conn.commit()

    _cur.close()

    print("++++++++++++++++++++++++++++++++++")


# def Q1(_conn):
#     print("++++++++++++++++++++++++++++++++++")
#     print("Q1")

#     try:
#         output = open('output/1.out', 'w')

#         header = "{:>10} {:<40} {:>10} {:>10} {:>10}"
#         output.write((header.format("wId", "wName", "wCap", "sId", "nId")) + '\n')

#         _cur = _conn.cursor()
#         _cur.execute("""
#         select * from warehouse
#         """)
#         w_content = _cur.fetchall()

#         for w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey in w_content:
#             output.write((header.format(w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey)) + '\n')
        
#         _conn.commit()
#         _cur.close()

#         output.close()
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")


# def Q2(_conn):
#     print("++++++++++++++++++++++++++++++++++")
#     print("Q2")



#     try:
#         _cur = _conn.cursor()
#         _cur.execute("""
#         select n_name as nation, count(w_warehousekey) as numW, sum(w_capacity) as totCap 
#         from warehouse, nation 
#         where n_nationkey = w_nationkey 
#         group by nation 
#         order by numW desc, totCap desc, n_name asc;
#         """)
#         queryContent = _cur.fetchall()

#         output = open('output/2.out', 'w')

#         header = "{:<40} {:>10} {:>10}"
#         output.write((header.format("nation", "numW", "totCap")) + '\n')

#         for nation, numW, totCap in queryContent:
#             output.write((header.format(nation, numW, totCap)) + '\n')
        
#         _conn.commit()
#         _cur.close()

#         output.close()
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")


# def Q3(_conn):
#     print("++++++++++++++++++++++++++++++++++")
#     print("Q3")

#     try:

#         input = open("input/3.in", "r")
#         nation = input.readline().strip()
#         input.close()

#         _cur = _conn.cursor()
#         _cur.execute("""
#         select s_name as supplier, n_name as nation, w_name as warehouse
#         from supplier, nation, warehouse 
#         where n_nationkey = w_nationkey and s_suppkey = w_suppkey
#         and n_name = (?) 
#         order by supplier;
#         """, (nation,))
#         queryContent = _cur.fetchall()

#         output = open('output/3.out', 'w')

#         header = "{:<20} {:<20} {:<40}"
#         output.write((header.format("supplier", "nation", "warehouse")) + '\n')

#         for supplier, nation, warehouse in queryContent:
#             output.write((header.format(supplier, nation, warehouse)) + '\n')
        
#         _conn.commit()
#         _cur.close()

#         output.close()
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")


# def Q4(_conn):
#     print("++++++++++++++++++++++++++++++++++")
#     print("Q4")

#     try:
#         input = open("input/4.in", "r")

#         cap = input.readline().strip()
#         input.close()

#         _cur = _conn.cursor()
#         _cur.execute("""
#         select w_name as warehouse, w_capacity as capacity 
#         from warehouse, nation, region
#         where w_nationkey = n_nationkey and n_regionkey = r_regionkey
#         and r_name = (?) and w_capacity > (?)
#         order by capacity desc;
#         """, (region,cap))
#         queryContent = _cur.fetchall()
        
#         output = open('output/4.out', 'w')

#         header = "{:<40} {:>10}"
#         output.write((header.format("warehouse", "capacity")) + '\n')

#         for warehouse, capacity in queryContent:
#             output.write((header.format(warehouse, capacity)) + '\n')
        
#         _conn.commit()
#         _cur.close()

#         output.close()
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")


# def Q5(_conn):
#     print("++++++++++++++++++++++++++++++++++")
#     print("Q5")

#     try:
#         input = open("input/5.in", "r")
#         nation = input.readline().strip()
#         input.close()

#         # select r_name as region, coalesce(sum(w_capacity), 0) as capacity
#         # from warehouse, supplier, nation SN, nation WN, region
#         # where w_suppkey = s_suppkey and s_nationkey = SN.n_nationkey and w_nationkey = WN.n_nationkey and WN.n_regionkey = r_regionkey
#         # and SN.n_name = "SAUDI ARABIA"
#         # group by region
#         # order by region asc;

#         _cur = _conn.cursor()
#         _cur.execute("""
#         select r_name as region, coalesce(sum(w_capacity), 0) as capacity
#         from warehouse, supplier, nation SN, nation WN, region
#         where w_suppkey = s_suppkey and s_nationkey = SN.n_nationkey and w_nationkey = WN.n_nationkey and WN.n_regionkey = r_regionkey
#         and SN.n_name = (?)
#         group by region
#         order by region asc;
#         """, (nation,))
#         queryContent = _cur.fetchall()

#         output = open('output/5.out', 'w')

#         RC = {}

#         for region, capacity in queryContent:
#             RC[region] = capacity
        
#         regions = ["AFRICA", "AMERICA", "ASIA", "EUROPE", "MIDDLE EAST"]

#         for location in regions:
#             if location not in RC.keys():
#                 RC[location] = 0
#         RC = sorted(RC.items())

#         # print(RC)

#         header = "{:<20} {:>20}"
#         output.write((header.format("region", "capacity")) + '\n')

#         for region, capacity in RC:
#             output.write((header.format(region, capacity)) + '\n')
        
#         # _conn.commit()
#         # _cur.close()

#         output.close()
#     except Error as e:
#         print(e)

#     print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"dealershipData.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        dropTable(conn)
        createTable(conn)
        populateTable(conn)

    # Q1(conn)
    # Q2(conn)
    # Q3(conn)
    # Q4(conn)
    # Q5(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
