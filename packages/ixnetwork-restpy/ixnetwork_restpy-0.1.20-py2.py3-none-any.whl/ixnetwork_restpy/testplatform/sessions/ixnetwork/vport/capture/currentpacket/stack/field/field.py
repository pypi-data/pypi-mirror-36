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
	def DisplayName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def FieldValue(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('fieldValue')

	def find(self, DisplayName=None, FieldValue=None):
		"""Finds and retrieves field data from the server.

		All named parameters support regex and can be used to selectively retrieve field data from the server.
		By default the find method takes no parameters and will retrieve all field data from the server.

		Args:
			DisplayName (str): 
			FieldValue (str): 

		Returns:
			self: This instance with found field data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
