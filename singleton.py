'''
An Abstract class for implementing the singleton pattern
'''

class Singleton:

	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._instance.__init__(*args, **kwargs)
		return cls._instance
	def __init__(self):
		assert False, "__init__ needs to be implemented"