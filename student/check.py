from django.db import connection

# Get a cursor object from the database connection
with connection.cursor() as cursor:
    # Use the cursor to execute SQL commands
    cursor.execute("DROP TABLE teacher;")
