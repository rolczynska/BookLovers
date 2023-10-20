# BookLovers - library app
> BookLovers bridges the gap between bibliophiles and their desired reads at the Biblioteka Raczyńskich in Poznań, ensuring they never miss out on a title they've been waiting for. 

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
The Raczyński Library in Poznań is a treasure trove for readers of all backgrounds. While it offers a website to check book availability, it lacked a feature to notify users about the availability of desired titles. BookLovers seamlessly fills this void. Users can save titles they're interested in, and the app checks the library's inventory daily. As soon as a title becomes available, it notifies the user via email. Whether for leisure reading or academic research, BookLovers ensures that no one misses out.


## Technologies Used
Language: Python 3.6
Web Framework: Flask 2.1.3
Template Engine: Jinja2
Database: firebase
Web Scraping: BeautifulSoup
Email Notification: yagmail
Testing: pytest
Text Processing: unidecode
Other Libraries: request, datetime, typing



## Features
View the current status of books across different branches of the Biblioteka Raczyńskich in Poznań.
Save and manage search preferences for future notifications.
Receive email notifications when a subscribed book becomes available.
Review and manage subscription details.

## Setup
Setting up BookLovers for local development is straightforward. Follow these steps to get the app up and running:

Prerequisites:
Ensure you have Python (version 3.6 or newer) installed on your system.
An active internet connection is needed to access external libraries and dependencies.



## Usage
Visit the BookLovers website.
Enter the desired book title.
Confirm the author and title from the provided suggestions.
If the book isn't available, choose your preferred library branches for subscription.
Once subscribed, the system will monitor the book's availability and notify you via email when it's ready to be borrowed.

## Contact
For further queries or feedback, reach out to [olkiewicz.alex@gmail.com].

