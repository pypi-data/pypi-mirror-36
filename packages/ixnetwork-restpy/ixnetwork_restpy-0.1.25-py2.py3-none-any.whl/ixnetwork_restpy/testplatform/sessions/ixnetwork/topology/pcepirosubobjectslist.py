from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PcepIroSubObjectsList(Base):
	"""The PcepIroSubObjectsList class encapsulates a system managed pcepIroSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PcepIroSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pcepIroSubObjectsList'

	def __init__(self, parent):
		super(PcepIroSubObjectsList, self).__init__(parent)

	@property
	def Active(self):
		"""Active

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('active')

	@property
	def AsNumber(self):
		"""AS Number

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('asNumber')

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
	def InterfaceId(self):
		"""Interface ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('interfaceId')

	@property
	def Ipv4Address(self):
		"""IPv4 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Address')

	@property
	def Ipv6Address(self):
		"""IPv6 Address

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Address')

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
	def PrefixLength(self):
		"""Prefix Length

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('prefixLength')

	@property
	def RouterId(self):
		"""Router ID

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('routerId')

	@property
	def SubObjectType(self):
		"""Sub Object Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves pcepIroSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve pcepIroSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all pcepIroSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with found pcepIroSubObjectsList data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
