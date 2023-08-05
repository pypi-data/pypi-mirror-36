from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MdLevels(Base):
	"""The MdLevels class encapsulates a system managed mdLevels node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the MdLevels property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'mdLevels'

	def __init__(self, parent):
		super(MdLevels, self).__init__(parent)

	@property
	def Active(self):
		"""Activate/Deactivate Configuration

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def BridgeId(self):
		"""Bridge ID

		Returns:
			list(str)
		"""
		return self._get_attribute('bridgeId')

	@property
	def Count(self):
		"""Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group

		Returns:
			number
		"""
		return self._get_attribute('count')

	@property
	def DescriptiveName(self):
		"""Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context

		Returns:
			str
		"""
		return self._get_attribute('descriptiveName')

	@property
	def MdMegLevel(self):
		"""MD/MEG Level

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdMegLevel')

	@property
	def MdName(self):
		"""MD Name For MAC + Int, Please Use MAC-Int eg. 11:22:33:44:55:66-1 For Others, Use Any String

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdName')

	@property
	def MdNameFormat(self):
		"""MD Name Format

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mdNameFormat')

	@property
	def Name(self):
		"""Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			str
		"""
		return self._get_attribute('name')
	@Name.setter
	def Name(self, value):
		self._set_attribute('name', value)

	@property
	def NumberOfMdLevels(self):
		"""Number of MD Levels

		Returns:
			number
		"""
		return self._get_attribute('numberOfMdLevels')
	@NumberOfMdLevels.setter
	def NumberOfMdLevels(self, value):
		self._set_attribute('numberOfMdLevels', value)

	def find(self, BridgeId=None, Count=None, DescriptiveName=None, Name=None, NumberOfMdLevels=None):
		"""Finds and retrieves mdLevels data from the server.

		All named parameters support regex and can be used to selectively retrieve mdLevels data from the server.
		By default the find method takes no parameters and will retrieve all mdLevels data from the server.

		Args:
			BridgeId (list(str)): Bridge ID
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			NumberOfMdLevels (number): Number of MD Levels

		Returns:
			self: This instance with found mdLevels data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
