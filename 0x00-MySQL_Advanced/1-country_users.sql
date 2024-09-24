-- This SQL script creates a MySQL table named 'users'
-- with the following columns:
--
-- 1. 'id' (INT): a unique identifier for each user
-- 2. 'email' (VARCHAR(255)): the email address of the user
-- 3. 'name' (VARCHAR(255)): the name of the user
-- 4. 'country' (ENUM('US', 'CO', 'TN')): the country of the user
--
-- The 'id' and 'email' columns are set to be not null and unique, meaning that each row in the table
-- must have a unique id and email. This table will be used to store information about users in our
-- application.
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `name` varchar(255),
  `country` ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_unique` (`email`)
);



