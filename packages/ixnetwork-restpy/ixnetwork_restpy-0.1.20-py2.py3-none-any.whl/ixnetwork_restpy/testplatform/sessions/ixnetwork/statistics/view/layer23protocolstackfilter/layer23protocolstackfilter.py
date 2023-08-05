from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23ProtocolStackFilter(Base):
	"""The Layer23ProtocolStackFilter class encapsulates a user managed layer23ProtocolStackFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer23ProtocolStackFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer23ProtocolStackFilter'

	def __init__(self, parent):
		super(Layer23ProtocolStackFilter, self).__init__(parent)

	@property
	def DrilldownType(self):
		"""

		Returns:
			str(perRange|perSession)
		"""
		return self._get_attribute('drilldownType')
	@DrilldownType.setter
	def DrilldownType(self, value):
		self._set_attribute('drilldownType', value)

	@property
	def NumberOfResults(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('numberOfResults')
	@NumberOfResults.setter
	def NumberOfResults(self, value):
		self._set_attribute('numberOfResults', value)

	@property
	def ProtocolStackFilterId(self):
		"""

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolStackFilter])
		"""
		return self._get_attribute('protocolStackFilterId')
	@ProtocolStackFilterId.setter
	def ProtocolStackFilterId(self, value):
		self._set_attribute('protocolStackFilterId', value)

	@property
	def SortAscending(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('sortAscending')
	@SortAscending.setter
	def SortAscending(self, value):
		self._set_attribute('sortAscending', value)

	@property
	def SortingStatistic(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=statistic)
		"""
		return self._get_attribute('sortingStatistic')
	@SortingStatistic.setter
	def SortingStatistic(self, value):
		self._set_attribute('sortingStatistic', value)

	def add(self, DrilldownType=None, NumberOfResults=None, ProtocolStackFilterId=None, SortAscending=None, SortingStatistic=None):
		"""Adds a new layer23ProtocolStackFilter node on the server and retrieves it in this instance.

		Args:
			DrilldownType (str(perRange|perSession)): 
			NumberOfResults (number): 
			ProtocolStackFilterId (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolStackFilter])): 
			SortAscending (bool): 
			SortingStatistic (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=statistic)): 

		Returns:
			self: This instance with all currently retrieved layer23ProtocolStackFilter data using find and the newly added layer23ProtocolStackFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer23ProtocolStackFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, DrilldownType=None, NumberOfResults=None, ProtocolStackFilterId=None, SortAscending=None, SortingStatistic=None):
		"""Finds and retrieves layer23ProtocolStackFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer23ProtocolStackFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer23ProtocolStackFilter data from the server.

		Args:
			DrilldownType (str(perRange|perSession)): 
			NumberOfResults (number): 
			ProtocolStackFilterId (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolStackFilter])): 
			SortAscending (bool): 
			SortingStatistic (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=statistic)): 

		Returns:
			self: This instance with found layer23ProtocolStackFilter data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
