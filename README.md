Goodreads.py connects to the Goodreads.com and Asana.com API. To connect to the
API you will need to grab and insert your personal access tokens, urser ids,
etc to the config.json file. In this file you can also specify your 'ideal
number of books to read' at any given time. The script uses this number to compare
against your "Currently Reading" bookshelf. If you have a reminder of N the
script will provide you with N book recommendations randomly selected from your
"To Read" shelf. The recommendations are created into N number of Asana tasks
in your specified project (though this can be easily changed to print the
recommendations). The task name == the book name and the description == the
summary of the book, ISBN, and a link back to goodreads.

Enjoy!
