from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Random(Base):
	"""The Random class encapsulates a system managed random node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Random property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'random'

	def __init__(self, parent):
		super(Random, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def Mask(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('mask')
	@Mask.setter
	def Mask(self, value):
		self._set_attribute('mask', value)

	@property
	def Width(self):
		"""

		Returns:
			str(16|24|32|8)
		"""
		return self._get_attribute('width')
	@Width.setter
	def Width(self, value):
		self._set_attribute('width', value)

	def find(self, AvailableWidths=None, Mask=None, Width=None):
		"""Finds and retrieves random data from the server.

		All named parameters support regex and can be used to selectively retrieve random data from the server.
		By default the find method takes no parameters and will retrieve all random data from the server.

		Args:
			AvailableWidths (list(str)): 
			Mask (str): 
			Width (str(16|24|32|8)): 

		Returns:
			self: This instance with found random data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
