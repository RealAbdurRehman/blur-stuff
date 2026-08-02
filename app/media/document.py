class Document:
    def __init__(self, pages):
        self.pages = pages

    def page(self, index):
        return self.pages[index]

    def __iter__(self):
        return iter(self.pages)

    def __len__(self):
        return len(self.pages)
