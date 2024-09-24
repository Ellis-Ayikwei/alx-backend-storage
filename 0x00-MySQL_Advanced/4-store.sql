-- Reduce item quantity when an order is made
-- Trigger created after an order is inserted
-- Decrease the quantity of an item by the number ordered
-- Trigger fires for each row that is inserted
-- Updates the quantity of an item by subtracting the number ordered
-- FROM NEW.number
-- WHERE name = NEW.item_name
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$
CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$
DELIMITER ;
