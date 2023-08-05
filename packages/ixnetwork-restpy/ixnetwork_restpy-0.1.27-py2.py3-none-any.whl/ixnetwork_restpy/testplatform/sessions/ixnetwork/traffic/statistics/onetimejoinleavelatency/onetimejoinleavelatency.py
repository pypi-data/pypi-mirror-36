from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class OneTimeJoinLeaveLatency(Base):
	"""The OneTimeJoinLeaveLatency class encapsulates a required oneTimeJoinLeaveLatency node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the OneTimeJoinLeaveLatency property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'oneTimeJoinLeaveLatency'

	def __init__(self, parent):
		super(OneTimeJoinLeaveLatency, self).__init__(parent)

	@property
	def Enabled(self):
		"""If true enables one time join leave latency.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
