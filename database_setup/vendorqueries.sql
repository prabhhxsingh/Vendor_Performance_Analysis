DROP DATABASE IF EXISTS vendor_performance;
CREATE DATABASE vendor_performance;
USE vendor_performance;

CREATE TABLE vendors (
    vendor_id INT PRIMARY KEY,
    vendor_name VARCHAR(100),
    contact_person VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    rating FLOAT
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    vendor_id INT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    discount FLOAT,
    total_sale DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE purchases (
    purchase_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    purchase_price DECIMAL(10,2),
    purchase_date DATE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


SELECT * FROM vendors;
SELECT * FROM products;
select *from sales;
select*from purchases;
SET GLOBAL local_infile = 1;
-- products table should reference vendors
ALTER TABLE products
ADD CONSTRAINT fk_vendor_id FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

-- sales table should reference products
ALTER TABLE sales
ADD CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(product_id);

-- purchases table should reference products
ALTER TABLE purchases
ADD CONSTRAINT fk_purchases_product FOREIGN KEY (product_id) REFERENCES products(product_id);

