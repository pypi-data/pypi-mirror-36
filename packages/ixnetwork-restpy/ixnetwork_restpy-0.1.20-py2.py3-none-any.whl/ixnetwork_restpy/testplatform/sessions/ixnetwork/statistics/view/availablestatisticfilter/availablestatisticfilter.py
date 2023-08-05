from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AvailableStatisticFilter(Base):
	"""The AvailableStatisticFilter class encapsulates a system managed availableStatisticFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AvailableStatisticFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'availableStatisticFilter'

	def __init__(self, parent):
		super(AvailableStatisticFilter, self).__init__(parent)

	@property
	def Caption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('caption')

	def find(self, Caption=None):
		"""Finds and retrieves availableStatisticFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve availableStatisticFilter data from the server.
		By default the find method takes no parameters and will retrieve all availableStatisticFilter data from the server.

		Args:
			Caption (str): 

		Returns:
			self: This instance with found availableStatisticFilter data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
