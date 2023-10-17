import time
from booklovers import database


def main():
    """Loop for searching books once per day"""
    while True:
        users = database.get_users()
        for user in users:
            mail = database.get_mail_obj(user)
            sent_books = mail.send()
            for key, item in sent_books.items():
                author, title = key.split(" ")
                database.remove_search(author=author, title=title, email=user)

        print("Already searched for all books. Go to sleep.")
        time.sleep(60 * 60 * 12)




# def run():
#     """Main stages on demanded books loop. It starts every day."""
#     print("Starting searching")
#     # Checks availability of books registered in database.
#     while True:
#         docs = database.db.collection('books').get()
#         for doc in docs:
#             book = doc.libraries_and_mails_to_dict()
#             url = book['url']
#             availability = parser.get_libraries_availability(url)
#             if availability[0] == 'Na półce':
#                 # Sends notification mail for all followers and delete book from database.
#                 mail.send_mail(title=book['title'], author=book['author'], emails=book['emails'])
#                 book_id = f'{book["author"]} "{book["title"]}"'
#                 database.db.collection('books').document(book_id).delete()
#         print("Already searched for all books. Go to sleep.")
#         time.sleep(60 * 60 * 12)
