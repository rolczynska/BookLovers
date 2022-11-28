# BooksForYou - library app
> This app allow you to get information about available books you are interested, in Biblioteka Raczyńskich library pl. Wolnosci Street in Poznań. 

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
Raczyński library is the public library in Poznań. They have a website to check book availability, but they don't have the option to notify users when a specific book will be available.
The Book Lovers app saves unavailable titles and checks the availability every day. When the books appear app will send an e-mail to subscribers. 


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

