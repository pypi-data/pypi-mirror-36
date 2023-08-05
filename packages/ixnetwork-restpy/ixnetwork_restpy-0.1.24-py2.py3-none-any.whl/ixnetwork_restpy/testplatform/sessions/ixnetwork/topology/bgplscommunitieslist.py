from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class BgpLsCommunitiesList(Base):
	"""The BgpLsCommunitiesList class encapsulates a system managed bgpLsCommunitiesList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the BgpLsCommunitiesList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'bgpLsCommunitiesList'

	def __init__(self, parent):
		super(BgpLsCommunitiesList, self).__init__(parent)

	@property
	def AsNumber(self):
		"""AS #

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
	def LastTwoOctets(self):
		"""Last Two Octets

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('lastTwoOctets')

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
	def Type(self):
		"""Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('type')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves bgpLsCommunitiesList data from the server.

		All named parameters support regex and can be used to selectively retrieve bgpLsCommunitiesList data from the server.
		By default the find method takes no parameters and will retrieve all bgpLsCommunitiesList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with found bgpLsCommunitiesList data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
