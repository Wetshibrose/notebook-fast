from .schema import Note, Author

author_1 = Author(name="Elvis")
author_2 = Author(name="Kelly")
author_3 = Author(name="James")

notes: list[Note] = [
    Note(text="This is awesome", author=author_1),
    Note(text="This is great", author=author_2),
    Note(text="This is superb", author=author_3),
]
