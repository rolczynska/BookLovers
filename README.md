# 📚 BookLovers - Library App
BookLovers bridges the gap between bibliophiles and their desired reads at the Biblioteka Raczyńskich in Poznań, ensuring they never miss out on a title they've been eagerly awaiting.

## 📌 Table of Contents
- [General Information](#general-information)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contact](#contact)
<!-- - [License](#license) -->

## 📔 General Information
The Raczyński Library in Poznań is a haven for readers from various walks of life. While the library offers a digital platform for checking book availability, it did not have a notification system for desired titles. This is where BookLovers steps in. Users can earmark titles of interest, and our app keeps a daily tab on the library's catalog. Upon availability of a title, users are promptly notified via email, ensuring that whether it's a leisure read or crucial research material, they're always in the loop.

## 💼 Technologies Used
- **Language:** Python 3.6
- **Web Framework:** Flask 2.1.3
- **Template Engine:** Jinja2
- **Database:** Firebase
- **Hosting & Deployment:** Google App Engine
- **Web Scraping:** BeautifulSoup
- **Email Notification:** yagmail
- **Testing:** pytest
- **Text Processing:** unidecode
- **Other Libraries:** request, datetime, typing

### Frontend Template Credits
The frontend design of this project was heavily influenced by [StartBootstrap/startbootstrap-grayscale](https://github.com/StartBootstrap/startbootstrap-grayscale) . A big thank you to the creators and contributors of this library for their excellent work. While the original templates provided a foundational structure, various modifications were made to align it better with the project's objectives.

## 🌟 Features
- 📖 Explore the real-time availability of books across various branches of the Biblioteka Raczyńskich in Poznań.

- 🚫 If a desired book is unavailable at certain library branches, users can subscribe for notifications across multiple branches of their choice.

- 📌 Set up subscriptions to be alerted when the sought-after title becomes available at any of the selected branches.

- 📧 Receive alerts when a book of interest is ready to be borrowed.

- 🔍 View active subscriptions. For those wishing to discontinue alerts, a link is provided in the subscription email.
  
## 🛠️ Setup
Setting up BookLovers locally is a breeze. Follow these steps:

### Prerequisites
- Ensure Python (version 3.6 or newer) is installed.
- A steady internet connection for fetching external libraries and dependencies.

### 1. **Installing Required Packages**
   - Initialize a virtual environment:
     ```bash
     python -m venv myenv
     ```

   - Activate the environment:
     - **Windows**:
       ```bash
       myenv\Scripts\activate
       ```

     - **Linux/Mac**:
       ```bash
       source myenv/bin/activate
       ```

   - Fetch the required packages:
     ```bash
     pip install -r requirements.txt
     ```

### 2. **Flask Application Setup**
   Pen down your Flask application and set up the necessary routes for user interaction. Here's a simple blueprint:

   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def index():
       return "Welcome to BookLovers!"


   if __name__ == "__main__":
       app.run(debug=True)
```
### 3. **Firebase Integration**

- Initiate: Visit Firebase Console and establish a new project.
- Integration:
   - Access the "Your apps" section in project settings.
   - Select your application type: Web, Android, or iOS.
   - Follow the displayed SDK setup steps.
- Data Structure: Strategically design your Firebase data schema to handle library data proficiently.

### 4. **Deployment**
Opt for your preferred cloud provider (e.g., Google Cloud, AWS, Azure) and trail their deployment guide to make your Flask app live.

**Voila!** Your app is ready to roll. Dive in and let us know if you encounter any snags or have feedback.

## 🚀 **Usage**
- Open the BookLovers platform on [booklovers-poznan.online](https://book-lovers-382216.lm.r.appspot.com)
- Punch in the book title you're hunting for.
- Validate the author and title from the given suggestions.
- In case the title is unavailable, earmark your favored library branches.
- Provide your email address. This is crucial as it will be used to notify you about the book's availability.
- Once subscribed, rest easy. We'll keep an eye out and ping you once the book is ready for borrowing.
- If at any point you wish to cancel the notification, simply follow the 'unsubscribe' link provided in the notification email.

## 💌 **Contact**
Got queries or feedback? Drop a line at [olkiewicz.alex@gmail.com](mailto:olkiewicz.alex@gmail.com).
