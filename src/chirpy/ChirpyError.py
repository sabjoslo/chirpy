import logging

class Error(Exception):
	def __init__(self):
		pass
	def log(self, llevel):
		msg = ('ChirpyError: '+self.__class__.__name__+': '+self.msg)
		if llevel == 'error':
			logging.error(msg)
		elif llevel == 'critical':
			logging.critical(msg)

class InputError(Error):
	def __init__(self, msg, llevel=False):
		self.msg = msg
		if llevel:
                        self.log(llevel)

	def __str__(self):
		return repr(self.msg)
