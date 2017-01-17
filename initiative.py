class Initiative:
    """Class defining an initiative with
    - its title
    - its content
    - its date of apparition
    - its opinion (for or against)
    """

    def __init__(self, title=None, content=None, date=None, opinion=None):
        self.title = title
        self.content = content
        self.date = date
        self.opinion = opinion


    def __repr__(self):
        return "{} - {} - {} - {}" \
               .format(self.date, self.title, self.content, self.opinion)


    def __str__(self):
        return "Initiative:\ndate: {}\nTitle: {}\nTexte: {}\n" \
               .format(self.date, self.title, self.content)
