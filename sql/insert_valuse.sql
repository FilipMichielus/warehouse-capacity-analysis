-- Insert values into Building table
INSERT INTO Building (address, long_name, shortcut)
VALUES
    (1, 'Main Logistics Building', 'ML'),
    (2, 'North Warehouse', 'NW'),
    (3, 'South Warehouse', 'SW'),
    (4, 'Assembly Building', 'AB'),
    (5, 'Distribution Center', 'DC'),
    (6, 'Spare Parts Building', 'SP');


-- Insert values into Areas table
INSERT INTO Areas (address, long_name, zone_address, building_address)
VALUES
    -- Building 1: 6 storages
    (1,  'DPL', NULL, 1),
    (2,  'KLT', NULL, 1),
    (3,  'MTR', NULL, 1),
    (4,  'RPK', NULL, 1),
    (5,  'SBC', NULL, 1),
    (6,  'VNX', NULL, 1),

    -- Building 2: 3 storages
    (7,  'WHN', NULL, 2),
    (8,  'WHS', NULL, 2),
    (9,  'WHE', NULL, 2),

    -- Building 3: 4 storages
    (10, 'ASM', NULL, 3),
    (11, 'PRT', NULL, 3),
    (12, 'PKG', NULL, 3),
    (13, 'BUF', NULL, 3),

    -- Building 4: 2 storages
    (14, 'LOG', NULL, 4),
    (15, 'SUP', NULL, 4),

    -- Building 5: 3 storages
    (16, 'DCN', NULL, 5),
    (17, 'DCS', NULL, 5),
    (18, 'DCR', NULL, 5),

    -- Building 6: 3 storages
    (19, 'SP1', NULL, 6),
    (20, 'SP2', NULL, 6),
    (21, 'SP3', NULL, 6);


-- Insert values into Storage_configuration table
INSERT INTO Storage_configuration(area_address, racks, columns_count, shelves)
VALUES
(1, 20, 15, 5),
(2, 10, 7, 4),
(3, 15, 7, 7),
(4, 10, 10, 4),
(5, 30, 7, 3),
(6, 5, 6, 5),

(7, 10, 11, 4),
(8, 15, 8, 8),
(9, 10, 12, 4),

(10, 7, 18, 5),
(11, 15, 15, 2),
(12, 10, 20, 3),
(13, 6, 7, 3),

(14, 20, 10, 5),
(15, 4, 20, 4),

(16, 15, 10, 5),
(17, 15, 11, 6),
(18, 15, 20, 3),

(19, 10, 12, 5),
(20, 7, 8, 5),
(21, 30, 7, 3);
