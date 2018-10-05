USE sakila;

# 1a. Display the first and last names of all actors from the table actor.

SELECT first_name, last_name
FROM actor;

# 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor
# Name.

SELECT concat(first_name, ' ', last_name) AS 'Actor Name'
FROM actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, 
# "Joe." What is one query would you use to obtain this information?

SELECT actor_id AS 'ID number', first_name, last_name
FROM actor
WHERE first_name='Joe';

# 2b. Find all actors whose last name contain the letters GEN:

SELECT actor_id AS 'ID number', first_name, last_name
FROM actor
WHERE last_name LIKE '%GEN%' or '%GEN' or 'GEN%';

# 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first 
# name, in that order:

SELECT actor_id AS 'ID number', last_name, first_name
FROM actor
WHERE last_name like '%LI%' or '%LI' or 'LI%';

# 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, 
# and China:

SELECT country_id, country 
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

# 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a 
# column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as 
# the difference between it and VARCHAR are significant).

ALTER TABLE actor
ADD COLUMN description BLOB NOT NULL;

# 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description
# column.

ALTER TABLE actor
DROP description;

# 4a. List the last names of actors, as well as how many actors have that last name.

SELECT last_name, COUNT(last_name) AS 'Total Last Names'
FROM actor
GROUP BY last_name;

# 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared
# by at least two actors.

SELECT last_name, COUNT(last_name) AS 'Total Last Names'
FROM actor
GROUP BY last_name
HAVING COUNT(last_name) > 1;

# 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to 
# fix the record.

SET sql_safe_updates = 0;

UPDATE actor
SET first_name = "HARPO"
WHERE first_name = "GROUCHO" and last_name = "WILLIAMS";

SET sql_safe_updates = 1;

# 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after 
# all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.

SET sql_safe_updates = 0;

UPDATE actor
SET first_name = "GROUCHO"
WHERE first_name = "HARPO" and last_name = "WILLIAMS";

SET sql_safe_updates = 1;

# 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
# Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html

SHOW CREATE TABLE address;

# Table: address
# Create Table: CREATE TABLE `address` (
 # `address_id` smallint(5)unsigned NOT NULL AUTO_INCREMENT,
 # `address` varchar(50) NOT NULL,
 # `address2` varchar(50) DEFAULT NULL,
 # `district` varchar(20) NOT NULL,
 # `city_id` smallint(5)unsigned NOT NULL,
 # `postal_code` varchar(10) DEFAULT NULL,
 # `phone` varchar(20) NOT NULL,
 # `location` geometry NOT NULL,
 # `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 # PRIMARY KEY (`address_id`),
 # KEY `idx_fk_city_id` (`city_id`),
 # SPATIAL KEY `idx_location` (`location`),
 # CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city`(`city_id`) ON UPDATE CASCADE

# 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use 
# the tables staff and address:

SELECT address.address_id, staff.first_name, staff.last_name, address.address
FROM staff
INNER JOIN address ON
staff.address_id = address.address_id;

# 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff 
# and payment.

SELECT staff.staff_id, SUM(payment.amount) AS 'Total Rung UP'
FROM staff
INNER JOIN payment ON
staff.staff_id = payment.staff_id
WHERE payment_date LIKE '2005-08%'
GROUP BY staff.staff_id;

# 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film.
# Use inner join.

SELECT film.title, COUNT(film_actor.actor_id) AS 'Number of Actors'
FROM film
INNER JOIN film_actor ON
film.film_id = film_actor.film_id
GROUP BY film.title;

# 6d. How many copies of the film Hunchback Impossible exist in the inventory system?

SELECT film.title, COUNT(inventory.store_id) AS 'Total Stored'
FROM film
INNER JOIN inventory ON
film.film_id = inventory.film_id
WHERE film.title = 'Hunchback Impossible';

# 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List
# the customers alphabetically by last name:

SELECT c.first_name, c.last_name, SUM(p.amount) AS 'Total Payment'
FROM customer c
INNER JOIN payment p ON
c.customer_id = p.customer_id
GROUP BY c.last_name;

# 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence,
# films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles 
# of movies starting with the letters K and Q whose language is English.

 SELECT title
 FROM film
 WHERE title LIKE 'K%' 
 OR title LIKE 'Q%' 
 AND language_id IN
(
  SELECT language_id
  FROM language
  WHERE name = 'English' 
);

# 7b. Use subqueries to display all actors who appear in the film Alone Trip.

 SELECT actor_id, first_name, last_name
 FROM actor
 WHERE actor_id IN
 (
  SELECT actor_id
  FROM film_actor
  WHERE film_id IN
  (
   SELECT film_id
   FROM film
   WHERE title = 'Alone Trip'
  )
 );

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses 
# of all Canadian customers. Use joins to retrieve this information.

SELECT *
FROM country con
INNER JOIN city ON
con.country_id=city.country_id
WHERE con.country = 'Canada';

SELECT *
FROM city
INNER JOIN address a ON
city.city_id = a.city_id
WHERE city.country_id =20;

SELECT cus.first_name, cus.last_name, cus.email
FROM address a
INNER JOIN customer cus ON
a.address_id = cus.address_id
WHERE cus.address_id IN (481, 468, 1 , 3, 193, 415, 441);

# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
# Identify all movies categorized as family films.

SELECT film.film_id, film.title
FROM film_category fc
INNER JOIN film ON
film.film_id = fc.film_id
WHERE fc.category_id=8;

# 7e. Display the most frequently rented movies in descending order.

SELECT film_id, title, rental_duration
FROM film
GROUP BY title
ORDER BY rental_duration DESC;

# 7f. Write a query to display how much business, in dollars, each store brought in.

SELECT p.staff_id, SUM(p.amount) AS 'Income ($)'
FROM payment p
INNER JOIN store s ON
p.staff_id = s.manager_staff_id
GROUP BY p.staff_id;

# 7g. Write a query to display for each store its store ID, city, and country.

SELECT *
FROM store s
INNER JOIN address a ON
s.address_id = a.address_id;

SELECT *
FROM address a
INNER JOIN city c ON
a.city_id = c.city_id
WHERE a.city_id IN (300, 576);

SELECT c.city, con.country
FROM city c
INNER JOIN country con ON
c.country_id = con.country_id
WHERE c.country_id IN (20, 8) AND c.city_id IN (300, 576);

# 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following 
# tables: category, film_category, inventory, payment, and rental.)

SELECT fc.category_id, c.name, COUNT(fc.category_id) AS 'Total'
FROM film_category fc
INNER JOIN category c ON
fc.category_id=c.category_id
GROUP BY fc.category_id
ORDER BY COUNT(fc.category_id) DESC;

# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by 
# gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can 
# substitute another query to create a view.

CREATE VIEW shayan AS
SELECT fc.category_id, c.name, COUNT(fc.category_id)
FROM film_category fc, category c
WHERE fc.category_id=c.category_id
GROUP BY fc.category_id
ORDER BY COUNT(fc.category_id) DESC;

# 8b. How would you display the view that you created in 8a?

SELECT * FROM shayan;

# 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

DROP VIEW shayan; 