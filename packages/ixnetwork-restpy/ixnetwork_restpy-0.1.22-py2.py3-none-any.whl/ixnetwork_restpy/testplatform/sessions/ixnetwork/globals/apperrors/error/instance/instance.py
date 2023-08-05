from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Instance(Base):
	"""The Instance class encapsulates a system managed instance node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Instance property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'instance'

	def __init__(self, parent):
		super(Instance, self).__init__(parent)

	@property
	def SourceValues(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('sourceValues')

	def find(self, SourceValues=None):
		"""Finds and retrieves instance data from the server.

		All named parameters support regex and can be used to selectively retrieve instance data from the server.
		By default the find method takes no parameters and will retrieve all instance data from the server.

		Args:
			SourceValues (list(str)): 

		Returns:
			self: This instance with found instance data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
