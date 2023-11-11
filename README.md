# HUB200 News | Capstone CS50W

## Overview

The project is designed as a website to showcase all the latest updates from Computiq company and our Hub200 workspace. Users who have not logged in can browse the website normally, but they won't have access to many options. For instance, they won't be able to subscribe to any category in the project. After a user subscribes to a category, their name is saved in the database. When any new content is added to that category by the admin, an email notification is automatically sent to the subscribed user. Additionally, there are control panel pages specifically for administrators who have the ability to perform CRUD operations on the entire database, including categories, articles, users, and more.

## Justification

This project meets all the expectations raised in the assignment of the CS50W final project, as it is a web platform that implements most of the concepts and techniques taught in the course.

The whole application is based on the Django framework, which allows managing user authentication, database models, HTTP requests, static files, and page rendering.

On the other hand, the user interface was designed with HTML, Tailwind CSS, and JS. The web application is mobile responsive. I have included the tailwind CSS library to make components/front-end mobile responsive.

The difference between this web application and previous projects is that this application makes use of and manages the data to show all newsletters ordered by date, create the news and categories, and comment on articles instantly. With the potential to include more features in the future with respect to other services such as the Vote & poll system, and more.

- [x] Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
- [x] Your web application must utilize Django (including at least one model) on the back end and JavaScript on the front end.
- [x] Your web application must be mobile-responsive.

## Structure

The web platform is structured as follows:

- myproject: the main Django project files like ( settings.py, urls.py )
- myapp: the main Django app like ( templates, static, views.py, urls.py )
- media: all Images on image fields in the database saved in this folder

## File Contents

### Front-End

---

- `/myapp/templates/` :
  - `layout.html` :
  - `index.html` :
  - `archives.html` :
  - `article.html` :
  - `categories.html` :
  - `category.html` :
  - `contact.html` :
  - `dashboard_articles.html` :
  - `dashboard_user.html` :
  - `dashboard_categories.html` :
  - `dashboard_layout.html` :
  - `dashboard_pagination.html` :
  - `editArticle.html` :
  - `editcategory.html` :
  - `editprofile.html` :
  - `editUser.html` :
  - `footer.html` :
  - `forget.html` :
  - `loadingpage.html` :
  - `newArticle.html` :
  - `news.html` :
  - `pagination.html` :
  - `passwordChange.html` :
  - `profile.html` :
  - `sendEmail.html` :
  - `signin.html` :
  - `signup.html` :
- `myapp/templates/django_social_share/templatetags` :
  - `post_to_facebook.html` :
  - `post_to_telegram.html` :
  - `post_to_twitter.html` :
  - `post_to_whatsapp.html` :
- `myapp/static` :
  - `brand.png` :
  - `category.svg` :
  - `home.svg` :
  - `hub.png` :
  - `login.svg` :
  - `main.js` :
  - `style.css` :
  - `signup.png` :
  - `whiteHUB.png` :
### Back-End

---

### Models in the app

There are 6 models for the web application's database.
  1. **User**: A fully featured User model with admin-compliant permissions.
  2. **Role**:  Holds the information about the roles for permissions and other
  3. **Category**:  Holds the information of all categories
  4. **Articles**: Holds the information of news and articles
  5. **Comments**: Holds the information of commenting system on articles

### Views files:

contains the functions for the web application. These view functions send and receive HTTP requests and responses.

### Manage.py file:

This file is used as a command-line utility and for deploying, debugging, or running the web application. This file contains code for runserver, makemigrations or migrations, etc. that we use in the shell. (Not changing anything here)

### urls.py files:

This file handles all the URLs of our Django web application. This file contains the lists of all the endpoints that we will have for our web application. Also, this file is like a link to the views in the app with the host web URL.

### admin.py files:

Similar to the name of the file, this file is used for registering the models into the Django administration. The models that are present have a superuser/admin who can control the information that is being stored. (they are pre-built)

### settings folder:

This file is present for adding all the applications and the middleware application present. This also has information about templates and databases. This is present in the main file of the Django web application.

### apps.py files:

This file deals with the application configuration of the apps. The default configuration is sufficient enough in most cases.

### models.py files:

This file contains the models of our web application (classes). They are the blueprints of the database we are using and hence contain the information regarding attributes and the fields, etc of the database.

### views.py files:

These files are the crucial ones, it contains all the views. This file can be considered as the file that interacts with the client.

# Installation & how to run the application

Run the application in its default port (Django: 8000).

## Run

```
virtualenv env
pip install -r requirements.txt
python manage.py runserver
```
