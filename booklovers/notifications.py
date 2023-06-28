import time
from booklovers import mail, parser, database


def run():
    """Main stages on demanded books loop. It starts every day."""
    print("Starting searching")
    # Checks availability of books registered in database.
    while True:
        docs = database.db.collection('books').get()
        for doc in docs:
            book = doc.to_dict()
            url = book['url']
            availability = parser.check_for_book_status(url)
            if availability == 'Na półce':
                # Sends notification mail for all followers and delete book from database.
                mail.send_mail(title=book['title'], author=book['author'], emails=book['emails'])
                book_id = f'{book["author"]} "{book["title"]}"'
                database.db.collection('books').document(book_id).delete()
        print("Already searched for all books. Go to sleep.")
        time.sleep(60 * 60 * 12)
