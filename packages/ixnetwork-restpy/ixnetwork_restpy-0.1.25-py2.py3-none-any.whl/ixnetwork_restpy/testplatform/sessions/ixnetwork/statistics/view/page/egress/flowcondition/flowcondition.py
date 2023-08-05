from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowCondition(Base):
	"""The FlowCondition class encapsulates a user managed flowCondition node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowCondition property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'flowCondition'

	def __init__(self, parent):
		super(FlowCondition, self).__init__(parent)

	@property
	def Operator(self):
		"""The logical operation to be performed.

		Returns:
			str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)
		"""
		return self._get_attribute('operator')
	@Operator.setter
	def Operator(self, value):
		self._set_attribute('operator', value)

	@property
	def ShowFirstMatchingSet(self):
		"""If true, displays the first matching set.

		Returns:
			bool
		"""
		return self._get_attribute('showFirstMatchingSet')
	@ShowFirstMatchingSet.setter
	def ShowFirstMatchingSet(self, value):
		self._set_attribute('showFirstMatchingSet', value)

	@property
	def TrackingFilterId(self):
		"""Selected tracking filters from the availableTrackingFilter list.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)
		"""
		return self._get_attribute('trackingFilterId')
	@TrackingFilterId.setter
	def TrackingFilterId(self, value):
		self._set_attribute('trackingFilterId', value)

	@property
	def Values(self):
		"""Value to be matched for the condition.

		Returns:
			list(number)
		"""
		return self._get_attribute('values')
	@Values.setter
	def Values(self, value):
		self._set_attribute('values', value)

	def add(self, Operator=None, ShowFirstMatchingSet=None, TrackingFilterId=None, Values=None):
		"""Adds a new flowCondition node on the server and retrieves it in this instance.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): The logical operation to be performed.
			ShowFirstMatchingSet (bool): If true, displays the first matching set.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
			Values (list(number)): Value to be matched for the condition.

		Returns:
			self: This instance with all currently retrieved flowCondition data using find and the newly added flowCondition data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the flowCondition data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Operator=None, ShowFirstMatchingSet=None, TrackingFilterId=None, Values=None):
		"""Finds and retrieves flowCondition data from the server.

		All named parameters support regex and can be used to selectively retrieve flowCondition data from the server.
		By default the find method takes no parameters and will retrieve all flowCondition data from the server.

		Args:
			Operator (str(isBetween|isDifferent|isEqual|isEqualOrGreater|isEqualOrSmaller|isGreater|isSmaller)): The logical operation to be performed.
			ShowFirstMatchingSet (bool): If true, displays the first matching set.
			TrackingFilterId (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTrackingFilter)): Selected tracking filters from the availableTrackingFilter list.
			Values (list(number)): Value to be matched for the condition.

		Returns:
			self: This instance with found flowCondition data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
