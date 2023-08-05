from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class StackLink(Base):
	"""The StackLink class encapsulates a system managed stackLink node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the StackLink property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'stackLink'

	def __init__(self, parent):
		super(StackLink, self).__init__(parent)

	@property
	def LinkedTo(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stackLink)
		"""
		return self._get_attribute('linkedTo')
	@LinkedTo.setter
	def LinkedTo(self, value):
		self._set_attribute('linkedTo', value)

	def find(self, LinkedTo=None):
		"""Finds and retrieves stackLink data from the server.

		All named parameters support regex and can be used to selectively retrieve stackLink data from the server.
		By default the find method takes no parameters and will retrieve all stackLink data from the server.

		Args:
			LinkedTo (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stackLink)): 

		Returns:
			self: This instance with found stackLink data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
