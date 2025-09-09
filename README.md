Link to PWS: https://pbp.cs.ui.ac.id/web/project/muhammad.vegard/footballshop

1. Explain how you implemented the checklist above step-by-step:

First, I created a new Django project and then generated an application named main inside it. After that, I made sure the application was registered in the project’s settings so Django could recognize it. To make the app the default entry point, I configured the main urls.py to include the routes defined in the main app.

Next, I built a Product model inside the main app with all the requested fields: name and category as character fields, price as an integer, description as a text field, thumbnail as a URL, and is_featured as a boolean. This provided the data structure for storing product information.

I then created a simple function in views.py that returned an HTML template. This template displayed the application name, my own name, and my class. To connect everything, I defined routes in the main/urls.py file that mapped directly to the view function.

Finally, I prepared the project for deployment to Pacil Web Service (PWS). This involved creating a project on the PWS dashboard, saving the provided credentials, configuring environment variables, and updating the settings.py file to include the deployment URL in ALLOWED_HOSTS. After committing and pushing the code to the remote repository, I deployed the app through PWS. Once the deployment status turned to “Running,” the project was accessible online for peers to view.

2. Create a diagram showing the client request to the Django-based web application and its response, and explain the relationship between urls.py, views.py, models.py, and the HTML file in the diagram.

Diagram: 
![Django Request-Response Flow](images/image.png)

HTTP Request → urls.py: When a client (browser) makes a request, Django first checks urls.py. This file acts like a traffic controller — it decides which view should handle the incoming URL.

urls.py → views.py: Once the request is matched, it is forwarded to the corresponding function (or class) inside views.py. The view is where the main logic lives: it decides whether to fetch data, process input, or simply render a page.

views.py ↔ models.py: If the view needs data from the database, it communicates with models.py. Models define the structure of the data and allow Django to read or write to the database through the ORM.

views.py → template (HTML): After gathering the necessary data, the view passes it into a template (.html file). Templates are responsible for presentation — they display the data in a user-friendly way using Django’s template language.

Template → HTTP Response: Finally, the template is rendered into a complete HTML page, which is sent back as the HTTP response to the client’s browser.

3. Explain the role of settings.py in a Django project!

In Django, the settings.py file is the main configuration hub of a project. It controls how the entire application behaves, both in development and in production. Instead of scattering configurations across different files, Django centralizes them in settings.py, making the project easier to manage and customize.
Some of the key roles of settings.py include:

~ Application setup: It lists all active apps in INSTALLED_APPS and middleware in MIDDLEWARE, which define what features and tools Django should load.

~ Database connection: It specifies database details such as engine, name, user, and password, so the project can connect and interact with data.

~ Static files and templates: It defines where CSS, JavaScript, images, and HTML templates are located and how Django should serve them.

~ Security: It holds sensitive configurations like SECRET_KEY, DEBUG, and ALLOWED_HOSTS, which ensure the project runs safely in different environments.

~ Localization: It manages language, timezone, and formatting to support users in different regions.

4. How does database migration work in Django?

In Django, database migration is the process of keeping your database schema (tables, columns, relationships) in sync with the models you define in your code. Instead of manually altering the database, Django automates this through migration files and commands.

~ Model changes: When you add, remove, or modify fields in your models (models.py), Django detects these changes.

~ Migration files: Running python manage.py makemigrations generates migration files inside the app’s migrations/ folder. These files are like versioned instructions that describe how the database should change (e.g., “add a new column price to the Product table”).

~ Applying migrations: Running python manage.py migrate applies those migration files to the actual database. Django translates them into SQL commands behind the scenes, updating tables without you writing SQL manually.

~ Version control: Each migration is numbered and linked, so Django knows the history of your database schema and can roll forward or backward if needed.

5. In your opinion, among all existing frameworks, why is the Django framework chosen as the starting point for learning software development?

In my opinion, Django gives a beginners a complete, structured, and practical environment to build real applications. Instead of forcing you to piece together many tools, Django comes with almost everything you need out of the box. In other words, beginner-friendly and very easy to use.

6. Do you have any feedback for the teaching assistant for Tutorial 1 that you previously completed?

So far, the explanation for the tutorial is clear, easy to understand.