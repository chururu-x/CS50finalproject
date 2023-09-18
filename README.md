# CS50 FINAL PROJECT:
Prism Dance - Pole Arts class reservation website

<br>

## Video Demo:
https://youtu.be/k8NerrlpWnoK

<br>

## Description:
A pole arts & dance class reservation website built using Python, HTML, Javascript and SQL.

Prospective students can view the classes that are available, and create an account to book their desired classes.

This is my final project for CS50 2023.

<br>

## Features:
1. Register & Login
2. Logout
3. Look up Classes and their respective timeslots
4. Add to and remove classes from Cart
5. Purchase classes ("purchase" without real money)
6. View booked classes
7. Leave and view Reviews

<br>

## File Structure:
1. `Main Directory`
    - `app.py` - Contains the main code for the website
    - `helpers.py` - Contains helper functions for the website which are imported into `app.py`
    - `pole.db` - Contains the database storing relevant data sent and received from the website. This includes users' login credentials (with hashing for passwords), details of pole dance classes such as the class name and timeslots, class booking details, as well as student reviews.

2. `templates` folder - contains the html code for all the webpages

3. `static` folder - contains the css stylesheet, as well as images and icons used

<br>

## Project Structure

### Home page
- In the Home page, you can navigate to different parts of the website using the navigation bar.
- There is also a direct link to the `/classes` page where you can view the classes offered by the studio.
- Anyone can access the Home Page. A registered account is not required.

<br>

### Classes page
- Displays classes offered by the studio (as card components). Users can view classes without a registered account.
- Clicking on the "Select Timing" button redirects users to another page where they can view & select the desired timeslot for a specific class. Only logged in users can view the timeslots. Non logged-in users are re-directed to the `/login` page.

<br>

### Timeslot pages for the respective classes
- Each class has its own timelsot page (e.g., `tricks-1.html`, `tricks-2.html`, etc.).
- Users can select a class timeslot from a dropdown list, which adds the timeslot & class to their cart and redirects them to the `/cart` page.
- Dropdown option for fully-booked classes are disabled.

<br>

### Cart page
- Displays all classes & timeslots that users have added to cart.
- Users can remove classes from Cart by clicking the `Remove` button.
- To simulate a purchase, users can click the `Buy` button. Users are redirected to the `/success` page upon successful purchase. From there, users can click a link to view their booked classes.
- Empty carts cannot be carted out and users will see an error.

<br>

### Your Reservations page
- Displays details of all the classes purchased (e.g. class name, timeslot, term and year).

<br>

### Reviews page
- Allows anyone to post reviews with a star rating system. Users do not need to be logged in to post a review.
- Displays all past reviews.

<br>

### Log In page
- Users log in by entering their email and password. Both are required fields
- If the email address or password cannot be found in the database, an apology (bad request error 404) is rendered.
- Upon successful login, users will be redirected to `/your-reservations` page
- Non logged in users can acccess the `/login` page or `/register` page at any time via the Navigation Bar.

<br>

### Register page
- Allows new users to register by entering details such as First Name, Last Name, Email and Password. All fields are required.
- The `email` field is validated, and users will receive an error message if a non-email format string is entered.
- The password is hashed for storage in the database, for security purposes
- Upon successful registration, users are redirected to the root index `/` (ie. Home page).

<br>

### Navigation Bar design
- Non logged in users can access the following pages at any time through the navigation bar: `/` (ie. Home page), `/classes`, `/reviews`, `/register`, `/login`.
- Logged in users can access the following pages at any time through the navigation bar: `/` (ie. Home page), `/classes`, `/cart`, `/your-reservations`, `/reviews`.
- Logged in users can log out by clicking the "Log Out" button at the top right of the Navigation Bar.

<br>

## Database Structure
- The `pole.db` database consists of 5 tables:

  - `users` table: stores user data, including names, email addresses and hashed passwords

  - `classes` table: stores the name and price of each classe (example: Tricks Level 1, $300)

  - `timings` table: stores class timeslots, term, year and booking count. This table has a foreign key (`class_id`) that references the `id` column in the `classes` table. The `booking_count` column is updated whenever a user carts out a class, in order to keep track of the number of students in each class.

  - `bookings` table: stores the details of each class booking. This table will be updated whenever a user carts out. The table includes the timestamp at which the booking was made, and several foreign keys that reference other tables.
    - FOREIGN KEY(`timing_id`) REFERENCES `timings(id)`
    - FOREIGN KEY(`user_id`) REFERENCES `users(id)`
    - FOREIGN KEY(`class_id`) REFERENCES `classes(id)`

  - `reviews` table: stores all reviews, including the timestamp at which the review was created

<br>

## Design Choices:
- **Website design**: The `/classes` and `/reviews` pages are avaialble to view even for users without a registered account. This allows prospective students to browse class types and see existing students' feedback.

- **Database design**: The `classes` and `timings` tables are separated to reduce data redundancy in the tables.

<br>

## Future Improvements:
- Implement a "pole reservation" feature for more advanced functionality.
- Add a "check out" feature to simulate the actual class purchase journey

<br>

## Acknowledgements:
- The project uses the following frameworks and libraries: os, re, cs50, Flask, werkzeug.security, Favicon, Memegen by Jace Browning.
- This project was inspired by my experience from booking classes at my current & past pole studios.
- All images used are from my personal professional photoshoots.

<br>

### Copyright:
All images used in this project are strictly not allowed for re-use in any private or public setting.
