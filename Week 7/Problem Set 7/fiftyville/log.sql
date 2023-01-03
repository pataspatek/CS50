-- See the description of the crime and get it's id.
SELECT description, id FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND street = "Humphrey Street";
-- At this time on this street happend two crimes, which the one with the duck has an id: 295. (297 is a different crime).

-- Description of the theft:
    --Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
    --Interviews were conducted today with three witnesses who were present at the time.
    --Each of their interview transcripts mentions the bakery.


-- Let's first take a look at the interwievs with witnesses
SELECT name, transcript FROM interviews
WHERE day = 28 AND month = 7;

-- Ruth:
    -- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
    -- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene:
    -- I don't know the thief's name, but it was someone I recognized.
    -- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond:
    -- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
    -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
    -- The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- Find the personal data of all people that left the bakery in ten minutes time frame after the theft (according to Ruth)
SELECT name, phone_number, passport_number FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = "exit";
-- +---------+----------------+-----------------+
-- |  name   |  phone_number  | passport_number |
-- +---------+----------------+-----------------+
-- | Vanessa | (725) 555-4692 | 2963008352      |
-- | Bruce   | (367) 555-5533 | 5773159633      |
-- | Barry   | (301) 555-4174 | 7526138472      |
-- | Luca    | (389) 555-5198 | 8496433585      |
-- | Sofia   | (130) 555-0289 | 1695452385      |
-- | Iman    | (829) 555-5269 | 7049073643      |
-- | Diana   | (770) 555-1861 | 3592750733      |
-- | Kelsey  | (499) 555-9472 | 8294398571      |
-- +---------+----------------+-----------------+


-- Find the person that was withdrawing money on the Legget Street on the day of the theft (according to Eugene) and combine the list with the people that left the bakery
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = "Leggett Street" AND atm_transactions.transaction_type = "withdraw" AND name IN (
    SELECT name FROM people
    JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
    WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = "exit"
);
-- +-------+
-- | name  |
-- +-------+
-- | Bruce |
-- | Diana |
-- | Iman  |
-- | Luca  |
-- +-------+

SELECT name, caller FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE day = 28 AND month = 7 AND duration < 60 AND caller IN (SELECT phone_number FROM people WHERE name IN (SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = "Leggett Street" AND atm_transactions.transaction_type = "withdraw" AND name IN (
    SELECT name FROM people
    JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
    WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = "exit"))
);

-- +--------+----------------+
-- |  name  |     caller     |
-- +--------+----------------+
-- | Robin  | (367) 555-5533 |
-- | Philip | (770) 555-1861 |
-- +--------+----------------+

SELECT * FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
JOIN passengers ON passengers.flight_id = flights.id
JOIN people ON people.passport_number = passengers.passport_number
WHERE origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") AND day = 29 AND month = 7 AND hour < 12 AND name IN (SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = "Leggett Street" AND atm_transactions.transaction_type = "withdraw" AND name IN (
    SELECT name FROM people
    JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
    WHERE day = 28 AND month = 7 AND hour = 10 AND minute <= 25 AND activity = "exit"
));


-- From this final tabel it is easy to figure out, that the thief was Bruce and his accomplice was Robin because of the Bruce phone number... he was the only possible suspect that called Robin 
-- +----+--------------+-------------------+---------------+----+-------------------+------------------------+------+-------+-----+------+--------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
-- | id | abbreviation |     full_name     |     city      | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | flight_id | passport_number | seat |   id   | name  |  phone_number  | passport_number | license_plate |
-- +----+--------------+-------------------+---------------+----+-------------------+------------------------+------+-------+-----+------+--------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+
-- | 4  | LGA          | LaGuardia Airport | New York City | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 36        | 5773159633      | 4A   | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 4  | LGA          | LaGuardia Airport | New York City | 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 36        | 8496433585      | 7B   | 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
-- +----+--------------+-------------------+---------------+----+-------------------+------------------------+------+-------+-----+------+--------+-----------+-----------------+------+--------+-------+----------------+-----------------+---------------+