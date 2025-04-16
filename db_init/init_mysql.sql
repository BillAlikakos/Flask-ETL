CREATE DATABASE IF NOT EXISTS eshop;
USE eshop;

CREATE TABLE clothes (
    clotheID VARCHAR(50) PRIMARY KEY,
    style ENUM('athletic', 'casual', 'formal', 'business'),
    color ENUM('Red', 'Green', 'Blue', 'Black', 'White'),
    brand VARCHAR(100) NOT NULL,
	price FLOAT NOT NULL
);

INSERT INTO clothes (clotheID, style, color, brand, price) VALUES
    ('C001', 'casual', 'Blue', 'Nike', 100.00),
    ('C002', 'athletic', 'Red', 'Adidas', 75.50),
    ('C003', 'formal', 'Black', 'Hugo Boss', 449.99),
    ('C004', 'business', 'White', 'Zara', 35.00),
    ('C005', 'casual', 'Green', 'Gap', 44.99),
    ('C006', 'casual', 'Black', 'Ecko Unltd', 99.99),
    ('C007', 'formal', 'Black', 'Gucci ', 249.99),
    ('C008', 'formal', 'White', 'Louis Vuitton', 339.99),
    ('C009', 'athletic', 'Blue', 'Asics', 59.99),
    ('C010', 'business', 'White', 'H&M', 69.99),
    ('C011', 'athletic', 'Green', 'Puma', 59.99),
    ('C012', 'casual', 'Black', 'Nike', 120.00),
    ('C013', 'athletic', 'Red', 'Adidas', 75.50),
    ('C014', 'formal', 'Black', 'Hugo Boss', 449.99),
    ('C015', 'business', 'White', 'Zara', 35.00),
    ('C016', 'business', 'Black', 'Argent', 59.99),
    ('C017', 'athletic', 'Blue', 'Adidas', 89.99),
    ('C018', 'formal', 'Black', 'Giorgio Armani', 349.99),
    ('C019', 'business', 'Black', 'Zara', 39.99),
    ('C020', 'athletic', 'Red', 'Puma', 59.99),
    ('C021', 'formal', 'White', 'Tommy Hilfiger', 119.99),
    ('C022', 'athletic', 'Black', 'Puma', 59.99);