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
- Raczyński librabry is the main public library in Poznań. They have a website to check books availability and a day of expected return. 
Unfortunatelly they don't have an option to notify you, when specific book will be available, or sigh in to reserve it, therby it is hard to get it.
If user really want to get the specific book, he should visiting website quite often to check is it already available.
The purpose of project is to check availability of specitif books that we are interested in and send an e-mail when it is available. 
As I live in Poznan and I use this library, I decided to make an app which resolve this problem. 



## Technologies Used
- Python - version 3.6
- request library
- BeautifulSoup library 
- yagmail library
- datetime library
- typing library
- pytest library



## Features
- checking book status
- sending an e-mail if it is available



## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?

Proceed to describe how to install / setup one's local environment / get started with the project.


## Usage
User have to provide an dictionary with url directing to website where book status is display. 

`{"Gdzie śpiewają raki": 'https://br-hip.pfsl.poznan.pl/ipac20/ipac.jsp?session=PI644T1937881.95392&profile=br-mar&uri=link=3100033~!2696598~!3100021~!3100029&aspect=basic_search&menu=search&ri=1&source=~!bracz&term=Gdzie+śpiewają+raki+%2F&index=ALTITLE'}`

