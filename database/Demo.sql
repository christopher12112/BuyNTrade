

--
-- Table structure for table `accounts`
--
USE `db`;-- put your databse name inside the single quote.
-- if you want to upload this sql to remote njit databse server, you need put your UCID inside the single quotes.

DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `categories`;


-- create the tables
CREATE TABLE products (
  productID         INT            NOT NULL   AUTO_INCREMENT,
  categoryID        INT            NOT NULL,
  productCode       VARCHAR(60)    NOT NULL,
  productName       VARCHAR(60)    DEFAULT NULL,
  listPrice         VARCHAR(40)    NOT NULL,
  PRIMARY KEY (productID)
);

CREATE TABLE categories (
  categoryID        INT            NOT NULL,
  categoryName      VARCHAR(60)    DEFAULT NULL,
  PRIMARY KEY (categoryID)
);

-- insert data into the database
INSERT INTO products (categoryID, productCode, productName,listPrice) VALUES
(1, 'strat', 'Fender Stratocaster', 699.00),
(1, 'les_paul', 'Gibson Les Paul', 1199.00),
(1, 'sg', 'Gibson SG', 2517.00),
(1, 'fg700s', 'Yamaha FG700s', 489.99),
(1, 'washburn', 'Washburn D10S', 299.00),
(1, 'rodriguez', 'Rodriguez Caballero 11', 415),
(2, 'precision', 'Fender Precision',799.99),
(2, 'hofner','Hofner Icon', 499.99),
(3,'ludwig','Ludwig 5-piece Drum Set with Cymbals',699.99),
(3, 'tama','Tama 5-piece Drum Set with Cymbals',799.99);

INSERT INTO categories (categoryID, categoryName) VALUES
(1, 'Guitars'),
(2, 'Basses'),
(3, 'Drums');
