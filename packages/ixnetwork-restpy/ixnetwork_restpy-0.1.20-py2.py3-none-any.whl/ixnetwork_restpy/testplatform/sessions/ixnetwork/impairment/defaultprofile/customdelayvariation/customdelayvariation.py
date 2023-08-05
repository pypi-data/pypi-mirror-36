from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class CustomDelayVariation(Base):
	"""The CustomDelayVariation class encapsulates a required customDelayVariation node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the CustomDelayVariation property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'customDelayVariation'

	def __init__(self, parent):
		super(CustomDelayVariation, self).__init__(parent)

	@property
	def CustomValue(self):
		"""An instance of the CustomValue class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.customdelayvariation.customvalue.customvalue.CustomValue)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.impairment.defaultprofile.customdelayvariation.customvalue.customvalue import CustomValue
		return CustomValue(self)

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

	@property
	def Name(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)
