from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Field(Base):
	"""The Field class encapsulates a system managed field node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Field property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'field'

	def __init__(self, parent):
		super(Field, self).__init__(parent)

	@property
	def __id__(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('__id__')

	@property
	def DisplayName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def FieldTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldTypeId')

	@property
	def Length(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('length')

	@property
	def Trackable(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('trackable')

	def find(self, __id__=None, DisplayName=None, FieldTypeId=None, Length=None, Trackable=None):
		"""Finds and retrieves field data from the server.

		All named parameters support regex and can be used to selectively retrieve field data from the server.
		By default the find method takes no parameters and will retrieve all field data from the server.

		Args:
			__id__ (str): 
			DisplayName (str): 
			FieldTypeId (str): 
			Length (number): 
			Trackable (bool): 

		Returns:
			self: This instance with found field data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
