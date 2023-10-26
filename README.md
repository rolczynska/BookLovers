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
- 📖 View the real-time availability of books across various branches of the Biblioteka Raczyńskich in Poznań.
- 📌 Bookmark and manage your search preferences for upcoming notifications.
- 📧 Get notified when a title you've subscribed to becomes available.
- 🔍 Review and adjust your subscription details seamlessly.

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
### 3. Firebase Integration
Head over to the [Firebase Console](https://console.firebase.google.com/) and initiate a new project.

Once set up, integrate Firebase with your app:
- Navigate to your project settings.
- Under "Your apps", choose the apt app type (Web, Android, iOS).
- Adhere to the SDK setup guidelines for a smooth Firebase integration.

Ensure your Firebase data structure is adeptly set up for efficient library data storage.

### 4. Deployment
Opt for your preferred cloud provider (e.g., Google Cloud, AWS, Azure) and trail their deployment guide to make your Flask app live.

**Voila!** Your app is ready to roll. Dive in and let us know if you encounter any snags or have feedback.

## 🚀 Usage
- Open the BookLovers platform on [booklovers-poznan.online](https://book-lovers-382216.lm.r.appspot.com)
- Punch in the book title you're hunting for.
- Validate the author and title from the given suggestions.
- In case the title is unavailable, earmark your favored library branches.
- After subscription, rest easy. We'll keep an eye out and ping you once the book is ready for borrowing.

## 💌 Contact
Got queries or feedback? Drop a line at [olkiewicz.alex@gmail.com](mailto:olkiewicz.alex@gmail.com).
