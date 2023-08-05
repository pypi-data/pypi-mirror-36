from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DrillDown(Base):
	"""The DrillDown class encapsulates a user managed drillDown node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DrillDown property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'drillDown'

	def __init__(self, parent):
		super(DrillDown, self).__init__(parent)

	@property
	def AvailableTargetRowFilters(self):
		"""An instance of the AvailableTargetRowFilters class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.availabletargetrowfilters.availabletargetrowfilters.AvailableTargetRowFilters)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.statistics.view.drilldown.availabletargetrowfilters.availabletargetrowfilters import AvailableTargetRowFilters
		return AvailableTargetRowFilters(self)

	@property
	def AvailableDrillDownOptions(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('availableDrillDownOptions')

	@property
	def TargetDrillDownOption(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('targetDrillDownOption')
	@TargetDrillDownOption.setter
	def TargetDrillDownOption(self, value):
		self._set_attribute('targetDrillDownOption', value)

	@property
	def TargetRow(self):
		"""

		Returns:
			list(str)
		"""
		return self._get_attribute('targetRow')

	@property
	def TargetRowFilter(self):
		"""

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)
		"""
		return self._get_attribute('targetRowFilter')
	@TargetRowFilter.setter
	def TargetRowFilter(self, value):
		self._set_attribute('targetRowFilter', value)

	@property
	def TargetRowIndex(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('targetRowIndex')
	@TargetRowIndex.setter
	def TargetRowIndex(self, value):
		self._set_attribute('targetRowIndex', value)

	def add(self, TargetDrillDownOption=None, TargetRowFilter=None, TargetRowIndex=None):
		"""Adds a new drillDown node on the server and retrieves it in this instance.

		Args:
			TargetDrillDownOption (str): 
			TargetRowFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)): 
			TargetRowIndex (number): 

		Returns:
			self: This instance with all currently retrieved drillDown data using find and the newly added drillDown data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the drillDown data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, AvailableDrillDownOptions=None, TargetDrillDownOption=None, TargetRow=None, TargetRowFilter=None, TargetRowIndex=None):
		"""Finds and retrieves drillDown data from the server.

		All named parameters support regex and can be used to selectively retrieve drillDown data from the server.
		By default the find method takes no parameters and will retrieve all drillDown data from the server.

		Args:
			AvailableDrillDownOptions (list(str)): 
			TargetDrillDownOption (str): 
			TargetRow (list(str)): 
			TargetRowFilter (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableTargetRowFilters)): 
			TargetRowIndex (number): 

		Returns:
			self: This instance with found drillDown data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def DoDrillDown(self):
		"""Executes the doDrillDown operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=drillDown)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('DoDrillDown', payload=locals(), response_object=None)
