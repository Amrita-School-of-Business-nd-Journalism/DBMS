USE DRONEDELIVERY;

SET @bhuvan_id = (
    SELECT USER_ID
    FROM USERS
    WHERE EMAIL = 'bhuvan@test.com'
);

INSERT INTO VENDORS
(VENDOR_ID, VENDOR_NAME, VENDOR_ADDRESS)
VALUES
(1, 'ABC Store', 'Coimbatore'),
(2, 'XYZ Electronics', 'Chennai');

-- ------------------------------------------------------------
-- 3. DRONES
-- ------------------------------------------------------------

INSERT INTO DRONES
(DRONE_ID, PAYLOAD_CAP, CURR_LOCATION, PURCHASE_DATE, LAST_DELIVERY)
VALUES
(
    1,
    5000,
    'Coimbatore',
    '2026-01-15',
    '2026-08-19 15:30:00'
),
(
    2,
    3000,
    'Chennai',
    '2026-02-10',
    '2026-08-18 12:00:00'
);

-- ------------------------------------------------------------
-- 4. BATTERIES
-- ------------------------------------------------------------

INSERT INTO BATTERIES
(BATTERY_ID, DRONE_ID, CAPACITY, CYCLES, STATUS)
VALUES
(1, 1, 5000, 120, 'GOOD'),
(2, 2, 4000, 80, 'GOOD');

-- ------------------------------------------------------------
-- 5. MAINTENANCE
-- ------------------------------------------------------------

INSERT INTO MAINTENACE
(MAINTENANCE_ID, DRONE_ID, STATUS, REPAIR_DATE, COST, REASON)
VALUES
(
    1,
    1,
    'GOOD',
    '2026-08-01',
    500,
    'Routine inspection'
);

-- ------------------------------------------------------------
-- 6. CHARGING SESSIONS
-- ------------------------------------------------------------

INSERT INTO CHARGING_SESSIONS
(BATTERY_ID, START_TIME, END_TIME)
VALUES
(
    1,
    '2026-08-20 08:00:00',
    '2026-08-20 09:30:00'
);

-- ------------------------------------------------------------
-- 7. PACKAGES
--
-- IMPORTANT:
-- USER_ID 1 = Bhuvan
-- VENDOR_ID 1 = ABC Store
-- ------------------------------------------------------------

INSERT INTO PACKAGES
(PACKAGE_ID, USER_ID, VENDOR_ID, PRODUCT_ID, WEIGHT, PRIORITY, STATUS)
VALUES
(1, @bhuvan_id, 1, 1001, 1500, 1, 'AVAILABLE'),
(2, @bhuvan_id, 1, 1002, 2000, 2, 'AVAILABLE'),
(3, @bhuvan_id, 2, 2001, 1000, 3, 'AVAILABLE');

-- ------------------------------------------------------------
-- 8. ROUTES
-- ------------------------------------------------------------

INSERT INTO ROUTES
(ROUTE_ID, SOURCE, DESTINATION, DISTANCE, ESTIMATED_TIME)
VALUES
(
    1,
    'Coimbatore',
    'Chennai',
    450.50,
    180
),
(
    2,
    'Coimbatore',
    'Bangalore',
    365.25,
    150
);

-- ------------------------------------------------------------
-- 9. MISSIONS
--
-- Package 1 -> ONGOING
-- Package 2 -> OVER
-- Package 3 -> IDLE
-- ------------------------------------------------------------

INSERT INTO MISSIONS
(
    MISSION_ID,
    DRONE_ID,
    PILOT_ID,
    PACKAGE_ID,
    ROUTE_ID,
    MISSION_STATUS,
    START_TIME,
    END_TIME
)
VALUES
(
    1,
    1,
    101,
    1,
    1,
    'ONGOING',
    '2026-08-20 10:00:00',
    '2026-08-20 13:00:00'
),
(
    2,
    2,
    102,
    2,
    2,
    'OVER',
    '2026-08-19 09:00:00',
    '2026-08-19 12:00:00'
),
(
    3,
    1,
    101,
    3,
    1,
    'IDLE',
    '2026-08-21 10:00:00',
    '2026-08-21 13:00:00'
);

-- ------------------------------------------------------------
-- 10. PAYMENTS
-- ------------------------------------------------------------

INSERT INTO PAYMENTS
(
    PAYMENT_ID,
    USER_ID,
    MISSION_ID,
    TIMESTAMP,
    MODE,
    AMOUNT,
    STATUS
)
VALUES
(
    1,
    1,
    1,
    '2026-08-20 09:30:00',
    'ONLINE',
    500,
    'PROCESSING'
),
(
    2,
    1,
    2,
    '2026-08-19 08:30:00',
    'ONLINE',
    750,
    'COMPLETED'
);

-- ============================================================
-- CHECK DATA
-- ============================================================

SELECT * FROM USERS;
SELECT * FROM VENDORS;
SELECT * FROM DRONES;
SELECT * FROM PACKAGES;
SELECT * FROM ROUTES;
SELECT * FROM MISSIONS;
SELECT * FROM PAYMENTS;