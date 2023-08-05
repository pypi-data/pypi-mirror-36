from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ValueList(Base):
	"""The ValueList class encapsulates a system managed valueList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ValueList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'valueList'

	def __init__(self, parent):
		super(ValueList, self).__init__(parent)

	@property
	def AvailableWidths(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('availableWidths')

	@property
	def StartValueList(self):
		"""

		Returns:
			list(number)
		"""
		return self._get_attribute('startValueList')
	@StartValueList.setter
	def StartValueList(self, value):
		self._set_attribute('startValueList', value)

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

	def find(self, AvailableWidths=None, StartValueList=None, Width=None):
		"""Finds and retrieves valueList data from the server.

		All named parameters support regex and can be used to selectively retrieve valueList data from the server.
		By default the find method takes no parameters and will retrieve all valueList data from the server.

		Args:
			AvailableWidths (list(str)): 
			StartValueList (list(number)): 
			Width (str(16|24|32|8)): 

		Returns:
			self: This instance with found valueList data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
