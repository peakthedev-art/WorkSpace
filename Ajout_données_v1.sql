-- =========================
-- INSERT ROLES (11)
-- =========================

INSERT INTO role (id, name)
VALUES
(UUID(), 'Administrateur'),
(UUID(), 'Agent'),
(UUID(), 'Technicien'),
(UUID(), 'Retraité'),
(UUID(), 'Visiteur');
(UUID(), 'Développeur logiciel'),
(UUID(), 'Administrateur système'),
(UUID(), 'Administrateur réseau'),
(UUID(), 'Ingénieur informatique'),
(UUID(), 'Chef de projet'),
(UUID(), 'Enfant de moins de 18 ans'),

-- =========================
-- INSERT BADGES (50)
-- =========================

INSERT INTO badge (id, activation_date, ending_date, role_id)
SELECT
    UUID(),
    activation_date,
    DATE_ADD(activation_date, INTERVAL FLOOR(RAND(4)*365) DAY),
    role.id
FROM (
    SELECT
        id,
        DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 365) DAY) AS activation_date
    FROM role
    LIMIT 50
) r;

-- =========================
-- INSERT UTILISATEURS (50)
-- =========================

INSERT INTO user (
    id,
    name,
    surname,
    birthdate,
    sex,
    email,
    badge_id
)
SELECT
    UUID(),
    CONCAT('Nom', ROW_NUMBER() OVER()),
    CONCAT('Prenom', ROW_NUMBER() OVER()),
    DATE_SUB(CURDATE(), INTERVAL (FLOOR(RAND()*40))*365 DAY),
    IF(RAND() > 0.5, 'M', 'F'),
    CONCAT('user', ROW_NUMBER() OVER(), '@workship-station.com'),
    badge.id
FROM badge b
LIMIT 50;

-- =========================
-- INSERT ZONES (20)
-- =========================

INSERT INTO zone(id, name)
VALUES
(UUID(), 'Passerelle de Commandement'),
(UUID(), 'Centre de Contrôle Navigation'),
(UUID(), 'Salle des Communications'),
(UUID(), 'Quartiers du Personnel'),
(UUID(), 'Quartiers des Cadres'),
(UUID(), 'Réfectoire Principal'),
(UUID(), 'Cuisine Centrale'),
(UUID(), 'Infirmerie'),
(UUID(), 'Laboratoire Scientifique'),
(UUID(), 'Centre de Recherche Biologique'),
(UUID(), 'Baie d’Ingénierie'),
(UUID(), 'Salle des Réacteurs'),
(UUID(), 'Centre de Distribution Énergétique'),
(UUID(), 'Hangar Principal'),
(UUID(), 'Baie de Maintenance'),
(UUID(), 'Entrepôt de Stockage'),
(UUID(), 'Jardin Hydroponique'),
(UUID(), 'Usine de Recyclage'),
(UUID(), 'Centre de Sécurité'),
(UUID(), 'Salle des Archives');


-- =========================
-- INSERT HABITATIONS (50)
-- =========================

INSERT INTO location (id, owner_id)
VALUES
('125 Oak Street, Austin, TX 78701', UUID()),
('125 Oak Street, Austin, TX 78701', UUID()),
('742 Evergreen Terrace, Springfield, IL 62704', UUID()),
('1600 Pennsylvania Avenue NW, Washington, DC 20500', UUID()),
('350 Fifth Avenue, New York, NY 10118', UUID()),
('221B Baker Avenue, Boston, MA 02108', UUID()),
('100 Market Street, San Francisco, CA 94105', UUID()),
('100 Market Street, San Francisco, CA 94105', UUID()),
('500 Sunset Boulevard, Los Angeles, CA 90028', UUID()),
('12 Palm Drive, Miami, FL 33101', UUID()),
('12 Palm Drive, Miami, FL 33101', UUID()),
('87 River Road, Portland, OR 97201', UUID()),
('145 Maple Avenue, Denver, CO 80202', UUID()),
('233 Pine Street, Seattle, WA 98101', UUID()),
('233 Pine Street, Seattle, WA 98101', UUID()),
('44 Liberty Lane, Philadelphia, PA 19103', UUID()),
('901 Elm Street, Dallas, TX 75201', UUID()),
('901 Elm Street, Dallas, TX 75201', UUID()),
('777 Lake View Drive, Chicago, IL 60601', UUID()),
('56 Cedar Court, Nashville, TN 37201', UUID()),
('290 Harbor Street, San Diego, CA 92101', UUID()),
('290 Harbor Street, San Diego, CA 92101', UUID()),
('18 Magnolia Way, Atlanta, GA 30303', UUID()),
('640 Grand Avenue, Phoenix, AZ 85004', UUID()),
('812 Forest Lane, Minneapolis, MN 55401', UUID()),
('812 Forest Lane, Minneapolis, MN 55401', UUID()),
('73 Willow Street, Charlotte, NC 28202', UUID()),
('154 Rosewood Drive, Orlando, FL 32801', UUID()),
('22 Highland Road, Salt Lake City, UT 84101', UUID()),
('312 Ocean Avenue, Virginia Beach, VA 23451', UUID()),
('312 Ocean Avenue, Virginia Beach, VA 23451', UUID()),
('978 King Street, Charleston, SC 29401', UUID()),
('48 Cherry Lane, Columbus, OH 43215', UUID()),
('48 Cherry Lane, Columbus, OH 43215', UUID()),
('605 Lincoln Street, Omaha, NE 68102', UUID()),
('810 Walnut Avenue, Kansas City, MO 64106', UUID()),
('1100 Constitution Drive, Richmond, VA 23219', UUID()),
('1100 Constitution Drive, Richmond, VA 23219', UUID()),
('95 Crystal Road, Albuquerque, NM 87102', UUID()),
('278 Green Street, Burlington, VT 05401', UUID()),
('771 Redwood Drive, Sacramento, CA 95814', UUID()),
('771 Redwood Drive, Sacramento, CA 95814', UUID()),
('980 Mountain View Road, Boise, ID 83702', UUID()),
('120 Riverfront Avenue, Pittsburgh, PA 15222', UUID()),
('120 Riverfront Avenue, Pittsburgh, PA 15222', UUID()),
('400 Freedom Street, Detroit, MI 48226', UUID()),
('555 Pioneer Trail, Helena, MT 59601', UUID()),
('88 Heritage Lane, Indianapolis, IN 46204', UUID()),
('88 Heritage Lane, Indianapolis, IN 46204', UUID()),
('701 Crescent Boulevard, New Orleans
INSERT, LA 70112', UUID());

-- =========================
-- INSERT ACCÈS ZONES (50)
-- =========================

INSERT INTO access_zone(role_id, zone_id)
VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 18),
(1, 20),
 
(2, 20),
(2, 5),
(2, 6),
(2, 19),
(2, 14),
 
(3, 12),
(3, 13),
(3, 15),
(3, 14),
(3, 17),
 
(4, 1),
(4, 2),
(4, 10),
(4, 18),
(4, 20),
 
(5, 6),
(5, 14),
(5, 5),
(5, 20),
(5, 3),
 
(6, 10),
(6, 9),
(6, 15),
(6, 13),
(6, 17),
 
(7, 12),
(7, 15),
(7, 17),
(7, 14),
(7, 13),
 
(8, 13),
(8, 12),
(8, 17),
(8, 15),
(8, 20),
 
(9, 19),
(9, 1),
(9, 2),
(9, 3),
(9, 18),

(10, 15),
(10, 12),
(10, 14),
(10, 13),
(10, 17);