from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class AllFlowsFilter(Base):
	"""The AllFlowsFilter class encapsulates a user managed allFlowsFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the AllFlowsFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'allFlowsFilter'

	def __init__(self, parent):
		super(AllFlowsFilter, self).__init__(parent)

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
	def SortByStatisticId(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)
		"""
		return self._get_attribute('sortByStatisticId')
	@SortByStatisticId.setter
	def SortByStatisticId(self, value):
		self._set_attribute('sortByStatisticId', value)

	@property
	def SortingCondition(self):
		"""

		Returns:
			str(bestPerformers|worstPerformers)
		"""
		return self._get_attribute('sortingCondition')
	@SortingCondition.setter
	def SortingCondition(self, value):
		self._set_attribute('sortingCondition', value)

	def add(self, NumberOfResults=None, SortByStatisticId=None, SortingCondition=None):
		"""Adds a new allFlowsFilter node on the server and retrieves it in this instance.

		Args:
			NumberOfResults (number): 
			SortByStatisticId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): 
			SortingCondition (str(bestPerformers|worstPerformers)): 

		Returns:
			self: This instance with all currently retrieved allFlowsFilter data using find and the newly added allFlowsFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the allFlowsFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, NumberOfResults=None, SortByStatisticId=None, SortingCondition=None):
		"""Finds and retrieves allFlowsFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve allFlowsFilter data from the server.
		By default the find method takes no parameters and will retrieve all allFlowsFilter data from the server.

		Args:
			NumberOfResults (number): 
			SortByStatisticId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableStatisticFilter)): 
			SortingCondition (str(bestPerformers|worstPerformers)): 

		Returns:
			self: This instance with found allFlowsFilter data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
