class Initiative:
	"""
	Class defining an initiative with
	- its title
	- its content
	- for or against
	"""

	def __init__(self, title=None, content=None):
		self.title, self.content = title, content
	def __repr__(self):
		return "Initiative: {}\nTexte: {}\n".format(self.title, self.content)
