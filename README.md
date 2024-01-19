# NoteApp :ledger:

### About :information_source:
A Django web application responsible for adding and managing notes.
The application was created as part of my engineering thesis.

NoteApp offers comprehensive functionalities, such as:
1. user authentication
2. adding different types of notes (test, with images, videos or files)
3. displaying, editing and deleting notes
4. notes search engine, filtering and sorting
5. notes categorization
6. setting reminders to the notes
7. sharing notes to other users
8. exporting notes to a zip file
9. notifications in app and email notifications
10. user profile tab with statistics
11. two language versions (Polish and English)
12. WCAG 2.1 (contrast, alt texts and possibility to use the app with keyboard)

### Technology :computer:
The application was written in Python using Django framework. Data is stored 
in PostgreSQL database. Front was built in HTML5, CSS, Bootstrap and JS.

Python libraries used in the project:
1. Django
2. os

JavaScript libraries used in the project:
1. Chart.js
2. FullCalendar

### How to use :gear:
Do following steps:
1. Clone the repository
2. Create .env file (Django secret key, database connection and email config)
3. Create venv
4. In terminal type `pip install -r requirements.txt`
5. Next run database migration typing `python manage.py migrate`
6. To run the server type `python manage.py runserver`

### Future plans :rocket:
1. Dockerize application
2. Sharing notes using custom urls
3. Possibility to add custom note categories