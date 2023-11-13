.headers on
-- Get vehicles make, model, color, miles and price based on location of dealership

-- SELECT v.v_make, v.v_model, v.v_color, v.v_miles, v.v_price
-- FROM vehicle v
-- JOIN inventory i ON v.v_vin = i.v_vin
-- JOIN dealership d ON i.d_id = d.d_id
-- WHERE d.d_city = 'Austin';


-- Get images url of a vehicle associated with a particular booking

-- SELECT p.p_url
-- FROM photo p
-- JOIN vehicle v ON v.v_vin = p.v_vin
-- JOIN bookingVehicle b ON v.v_vin = b.v_vin
-- WHERE b.b_id = 5;

-- A dealer getting booking date, customer name and customer email for November 2023

-- SELECT b.b_date, c.c_name, c.c_email
-- FROM booking b
-- JOIN dealership d ON b.d_id = d.d_id
-- JOIN customer c ON b.c_id = c.c_id
-- WHERE d.d_id = 11 AND strftime('%m', b.b_date) = '11' AND strftime('%Y', b.b_date) = '2023';


-- Customer filtering vehicle based on color(either blue or purple), miles and price

-- SELECT v_vin, v_make, v_model, v_color, v_year, v_miles, v_price
-- FROM vehicle
-- WHERE (v_color = 'blue' OR v_color = 'purple') AND v_miles BETWEEN 10000 AND 20000 AND v_price < 30000;


-- A person registering on the website for the first time as a customer

-- INSERT INTO customer (c_name, c_phone, c_email)
-- VALUES ('Michael James', '1234567890', 'michael@gmail.com');

-- INSERT INTO customerVisit (d_id, c_id)
-- VALUES (14, (
--     SELECT c_id FROM customer WHERE c_name = 'Michael James' AND c_phone = '1234567890' AND c_email = 'michael@gmail.com'
--     )
-- );

-- How many employees are there in a particular city

-- SELECT COUNT(*)
-- FROM employee e
-- JOIN dealership d ON e.d_id = d.d_id
-- WHERE d.d_city = 'Brooklyn';


-- Average miles of vehicles in a particular state

-- SELECT AVG(v.v_miles)
-- FROM vehicle v
-- JOIN inventory i ON v.v_vin = i.v_vin
-- JOIN dealership d ON i.d_id = d.d_id
-- WHERE d.d_state = 'Texas';


-- Highest prices of cars from all make by model year

-- SELECT v.v_year, MAX(v.v_price)
-- FROM vehicle v
-- GROUP BY v.v_year;


-- Update the city name 'San Jose' to 'Lafayette' as the city name has been changed in California

-- UPDATE dealership 
-- SET d_city = 'Lafayette' 
-- WHERE d_city = 'San Diego' AND d_state = 'California';


-- It is noticed that the dealer with the dealership id of 19 is a fake dealer. Deleting the dealer altogether: bookings, inventory, etc. of this dealer

-- DELETE FROM dealership WHERE d_id = 19;

-- DELETE FROM inventory WHERE d_id = 19;

-- DELETE FROM customerVisit WHERE d_id = 19;

-- DELETE FROM employee WHERE d_id = 19;

-- DELETE FROM booking WHERE d_id = 19;



-- How many cars arrived in each month during the year 2022

-- SELECT strftime('%m', i_dateOfArrival), COUNT(*)
-- FROM inventory
-- WHERE strftime('%Y', i_dateOfArrival) = '2022'
-- GROUP BY strftime('%m', i_dateOfArrival);


-- Which employees of 'Hills-Will' have bookings in the month of October 2023

-- SELECT e.e_name, COUNT(*)
-- FROM employee e
-- JOIN booking b ON e.e_id = b.e_id
-- JOIN dealership d ON e.d_id = d.d_id
-- -- WHERE d.d_name = 'Hills-Will' and strftime('%m', b.b_date) = '11'
-- GROUP BY e.e_id, e.e_name;


-- A customer books an appointment, only five values are needed since b_id is primary key auto increment

-- INSERT INTO booking (b_date, b_time, c_id, e_id, d_id)
-- VALUES ('2023-11-09', '10:30 AM', 8, 5, 14);


-- A customer searching for cars not older than 5 years

-- SELECT v.v_make, v.v_model, v.v_color, v.v_miles, v.v_price, v.v_year
-- FROM vehicle v
-- WHERE ((
--     SELECT MAX(strftime('%Y', b.b_date)) from booking b
-- ) - v.v_year) <= 5;


-- A dealership is closing its business and hence, it's data has to be removed first then its id.

-- DELETE FROM inventory WHERE d_id = (SELECT d_id FROM dealership WHERE d_name = 'Abbott-Stark');

-- DELETE FROM customerVisit WHERE d_id = (SELECT d_id FROM dealership WHERE d_name = 'Abbott-Stark');

-- DELETE FROM employee WHERE d_id = (SELECT d_id FROM dealership WHERE d_name = 'Abbott-Stark');

-- DELETE FROM booking WHERE d_id = (SELECT d_id FROM dealership WHERE d_name = 'Abbott-Stark');

-- DELETE FROM dealership WHERE d_name = 'Abbott-Stark';


-- 'Hills and Sons' is moving from 'Atlanta' to 'San Francisco' and is updating its city but and state, using ID instead of name and city as identifier because there could be more than 1 Hills and Sons in Atlanta city and if that's the case it would change the city and state for all of those


-- UPDATE dealership
-- SET d_city = 'San Francisco', d_state = 'CA'
-- WHERE d_id = 5;


-- A dealership with ID 17 has purchased 5 old cars on 2023-11-5

-- INSERT INTO inventory (v_vin, i_dateofarrival, d_id)
-- VALUES
--     ('ABC123120ZKLEWR78', '2023-11-05', 17),
--     ('DEF456DF88B23J4K1', '2023-11-05', 17),
--     ('GHI789J34BSKDF783', '2023-11-05', 17),
--     ('JKL012LD0F823B6F1', '2023-11-05', 17),
--     ('MNO345CD6X21CE88C', '2023-11-05', 17);

-- 4 cars have sold

-- DELETE FROM inventory
-- WHERE v_vin IN ('1FT8W3DT3GEC61076', '1GTR1UEH7EZ264149', '1J4GL48K63W700412', '1GYS3DEF8BR175139');


-- Two dealerships with 10 and 16 are merging to be one, the new dealership will have the address and all other details of dealership with ID 10 and all the inventory, employees, customers and bookings of dealership 16 will be transferred to ID 10

-- UPDATE inventory
-- SET d_id = 10
-- WHERE d_id = 16;

-- UPDATE booking
-- SET d_id = 10
-- WHERE d_id = 16;

-- UPDATE customerVisit
-- SET d_id = 10
-- WHERE d_id = 16;

-- UPDATE employee
-- SET d_id = 10
-- WHERE d_id = 16;

-- DELETE FROM dealership
-- WHERE d_id = 16;


-- Dealership 86 has fired all all the employees who didn't make more than 10 bookings in the year of 2022

-- DELETE FROM employee
-- WHERE e_id IN (
-- 	SELECT e.e_id
-- 	FROM employee e
-- 	JOIN booking b ON e.e_id = b.e_id
--     JOIN dealership d ON d.d_id = b.d_id
-- 	WHERE strftime('%Y', b.b_date) = '2022' AND e.d_id = 89
-- 	GROUP BY e.e_id
-- 	HAVING COUNT(*) <= 10
-- );