-- Created by Ellis Armah Ayikwei
-- This SQL script creates a MySQL table named 'users'
-- with the following columns:
--
-- 1. 'id' (INT): a unique identifier for each user
-- 2. 'email' (VARCHAR(255)): the email address of the user
-- 3. 'name' (VARCHAR(255)): the name of the user
--
-- The 'id' column is set to be not null and unique, meaning that each row in the table
-- must have a unique id. This table will be used to store information about users in our
-- application.
CREATE TABLE `users` IF NOT EXISTS(
    `id` INT NOT NULL UNIQUE,
    `email` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255),
    PRIMARY KEY (`id`)
)