
searching_titles = {}


def add_to_list(title, email):
    if title in searching_titles:
        searching_titles[title].append(email)
    else:
        searching_titles[title] = email


def is_already_registered(title, email):
    pass
