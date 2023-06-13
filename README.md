# BooksForYou - library app
> This app allows you to get information about available books you are interested, in Biblioteka Raczyńskich library pl. Wolności Street in Poznań. 

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
Raczyński Library, located in Poznań, is a public library that houses a vast collection of books for book lovers of all ages. While they do have a website that allows users to check the availability of books, they currently do not offer the option to notify users when a specific book becomes available.

To solve this problem, the Book Lovers app has stepped in to provide a solution. The app allows users to save titles of books they are interested in that may currently be unavailable at the library. The app then checks the library's inventory every day, and as soon as the book becomes available, it sends an email notification to the subscriber.

This handy feature ensures that book lovers never miss out on the opportunity to borrow a book from the Raczyński Library. Whether you're an avid reader or a student looking for research material, the Book Lovers app is the perfect tool to help you stay on top of the library's inventory and keep track of your favorite books.

## Technologies Used
- Python - version 3.6
- Flask - 2.1.3
- request library
- BeautifulSoup library 
- yagmail library
- datetime library
- typing library
- pytest library
- unidecode library




## Features
- checking book status
- sending an e-mail if book is available
- checking users subscriptions 



## Setup
All requirements are in the requirements.txt

Proceed to describe how to install / setup one's local environment / get started with the project.


## Usage
User visit a website, enter a title of searching book and confirm author and title. If book is not available, he can subscribe by enter an email. 

