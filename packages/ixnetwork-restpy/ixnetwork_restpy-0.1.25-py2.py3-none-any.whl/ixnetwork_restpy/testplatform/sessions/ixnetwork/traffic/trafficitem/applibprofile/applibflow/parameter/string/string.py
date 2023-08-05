from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class String(Base):
	"""The String class encapsulates a system managed string node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the String property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'string'

	def __init__(self, parent):
		super(String, self).__init__(parent)

	@property
	def Default(self):
		"""(Read only) Parameter default value.

		Returns:
			str
		"""
		return self._get_attribute('default')

	@property
	def Value(self):
		"""Parameter string value.

		Returns:
			str
		"""
		return self._get_attribute('value')
	@Value.setter
	def Value(self, value):
		self._set_attribute('value', value)

	def find(self, Default=None, Value=None):
		"""Finds and retrieves string data from the server.

		All named parameters support regex and can be used to selectively retrieve string data from the server.
		By default the find method takes no parameters and will retrieve all string data from the server.

		Args:
			Default (str): (Read only) Parameter default value.
			Value (str): Parameter string value.

		Returns:
			self: This instance with found string data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
