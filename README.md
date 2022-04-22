# WELCOME TO Omnino !

## Creators!
Team Name: Group 8
 * Tayo Rufai (orufai1@student.gsu.edu)
 * Ryan Garland (rgarland2@student.gsu.edu)
 * Malia Absi (mabsi2@student.gsu.edu)
 * Michael Fralish (mfralish2@student.gsu.edu)

## If you want to see what we've been working on, just visit the link below
[Heroku Link](https://omnino.herokuapp.com/)

## Linting
In app.py

pylint: disable=no-member
There were many instances in our code that resulted in this linting error. This was due to us using a scoped session of sqlAlchemy. It claimed that we did not have an instance of add, commit, or delete in the scoped session, although these commands very clearly do work.

pylint: disable=invalid-envvar-default
There was one instance of this error in the line last line of this file, to run the app. It says that os.getenv default type is a string, for the port where we have proveded port number 8080. This is correct and is default code provided in class.

pylint: disable=too-many-locals
We have two functions in our code, visit_singular_community() and profile_page(), that we used greater than 15 local variables. We determened that all usage of these variables was necessary to our objective, so we disabled the linting warning.


In models.py

pylint: disable=no-member
The error indicated that our instance SQLAlchemy did not have Column, String, or Integer as a member. This is clearly not the case, as our program allows us to make these data types within our database.

pylint: disable=too-few-public-methods
This error declared that we needed to have at least two public methods in each class in our database. As these classes were to only represent db tables, they did not require any public methods.


In stytch_tools.py

pylint: disable=protected-access
There were three instances in which we needed to access information in the _content of the response from stytch. As I could determine from the printout of the response, there was no other way to access this information, so this alert was disabled.


In unit_tests.py

pylint: disable=unused-variable
This was disabled because it was incorrectly interpreting our with statements that we used to patch during our unit tests.



## Goal
Our objective is to deliver an app that is browser and mobile accessible. (Will not be available on Google Play or the App Store). The app will be used to help activists join with like minded individuals by either finding a community such as a Discord server, donating to a charity with similar goals, or posting or signing up to participate in a demonstration or event.


 

