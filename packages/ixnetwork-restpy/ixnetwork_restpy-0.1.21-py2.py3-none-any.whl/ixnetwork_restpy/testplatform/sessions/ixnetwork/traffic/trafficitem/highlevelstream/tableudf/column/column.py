from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Column(Base):
	"""The Column class encapsulates a user managed column node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Column property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'column'

	def __init__(self, parent):
		super(Column, self).__init__(parent)

	@property
	def Format(self):
		"""

		Returns:
			str(ascii|binary|custom|decimal|hex|ipv4|ipv6|mac)
		"""
		return self._get_attribute('format')
	@Format.setter
	def Format(self, value):
		self._set_attribute('format', value)

	@property
	def Offset(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('offset')
	@Offset.setter
	def Offset(self, value):
		self._set_attribute('offset', value)

	@property
	def Size(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('size')
	@Size.setter
	def Size(self, value):
		self._set_attribute('size', value)

	@property
	def Values(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def add(self, Format=None, Offset=None, Size=None, Values=None):
		"""Adds a new column node on the server and retrieves it in this instance.

		Args:
			Format (str(ascii|binary|custom|decimal|hex|ipv4|ipv6|mac)): 
			Offset (number): 
			Size (number): 
			Values (list(str)): 

		Returns:
			self: This instance with all currently retrieved column data using find and the newly added column data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the column data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Format=None, Offset=None, Size=None, Values=None):
		"""Finds and retrieves column data from the server.

		All named parameters support regex and can be used to selectively retrieve column data from the server.
		By default the find method takes no parameters and will retrieve all column data from the server.

		Args:
			Format (str(ascii|binary|custom|decimal|hex|ipv4|ipv6|mac)): 
			Offset (number): 
			Size (number): 
			Values (list(str)): 

		Returns:
			self: This instance with found column data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
