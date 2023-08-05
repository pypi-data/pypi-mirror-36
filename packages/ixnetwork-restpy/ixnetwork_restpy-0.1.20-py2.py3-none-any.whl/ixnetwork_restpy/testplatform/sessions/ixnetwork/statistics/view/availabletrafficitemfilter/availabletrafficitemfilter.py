from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableTrafficItemFilter(Base):
	"""The AvailableTrafficItemFilter class encapsulates a system managed availableTrafficItemFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableTrafficItemFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableTrafficItemFilter'

	def __init__(self, parent):
		super(AvailableTrafficItemFilter, self).__init__(parent)

	@property
	def Constraints(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('constraints')

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')

	def find(self, Constraints=None, Name=None):
		"""Finds and retrieves availableTrafficItemFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableTrafficItemFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableTrafficItemFilter data from the server.

		Args:
			Constraints (list(str)): 
			Name (str): 

		Returns:
			self: This instance with found availableTrafficItemFilter data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
