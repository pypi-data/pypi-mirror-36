from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class InterArrivalTimeRate(Base):
	"""The InterArrivalTimeRate class encapsulates a required interArrivalTimeRate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the InterArrivalTimeRate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'interArrivalTimeRate'

	def __init__(self, parent):
		super(InterArrivalTimeRate, self).__init__(parent)

	@property
	def Enabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)
