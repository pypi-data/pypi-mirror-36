from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Uds(Base):
	"""The Uds class encapsulates a system managed uds node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Uds property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'uds'

	def __init__(self, parent):
		super(Uds, self).__init__(parent)

	@property
	def CustomFrameSizeFrom(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('customFrameSizeFrom')
	@CustomFrameSizeFrom.setter
	def CustomFrameSizeFrom(self, value):
		self._set_attribute('customFrameSizeFrom', value)

	@property
	def CustomFrameSizeTo(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('customFrameSizeTo')
	@CustomFrameSizeTo.setter
	def CustomFrameSizeTo(self, value):
		self._set_attribute('customFrameSizeTo', value)

	@property
	def DestinationAddressSelector(self):
		"""

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('destinationAddressSelector')
	@DestinationAddressSelector.setter
	def DestinationAddressSelector(self, value):
		self._set_attribute('destinationAddressSelector', value)

	@property
	def Error(self):
		"""

		Returns:
			str(errAnyFrame|errBadCRC|errBadFrame|errGoodFrame)
		"""
		return self._get_attribute('error')
	@Error.setter
	def Error(self, value):
		self._set_attribute('error', value)

	@property
	def FrameSizeType(self):
		"""

		Returns:
			str(any|custom|jumbo|oversized|undersized)
		"""
		return self._get_attribute('frameSizeType')
	@FrameSizeType.setter
	def FrameSizeType(self, value):
		self._set_attribute('frameSizeType', value)

	@property
	def IsEnabled(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('isEnabled')
	@IsEnabled.setter
	def IsEnabled(self, value):
		self._set_attribute('isEnabled', value)

	@property
	def PatternSelector(self):
		"""

		Returns:
			str(anyPattern|notPattern1|notPattern2|pattern1|pattern2)
		"""
		return self._get_attribute('patternSelector')
	@PatternSelector.setter
	def PatternSelector(self, value):
		self._set_attribute('patternSelector', value)

	@property
	def SourceAddressSelector(self):
		"""

		Returns:
			str(addr1|addr2|anyAddr|notAddr1|notAddr2)
		"""
		return self._get_attribute('sourceAddressSelector')
	@SourceAddressSelector.setter
	def SourceAddressSelector(self, value):
		self._set_attribute('sourceAddressSelector', value)

	def find(self, CustomFrameSizeFrom=None, CustomFrameSizeTo=None, DestinationAddressSelector=None, Error=None, FrameSizeType=None, IsEnabled=None, PatternSelector=None, SourceAddressSelector=None):
		"""Finds and retrieves uds data from the server.

		All named parameters support regex and can be used to selectively retrieve uds data from the server.
		By default the find method takes no parameters and will retrieve all uds data from the server.

		Args:
			CustomFrameSizeFrom (number): 
			CustomFrameSizeTo (number): 
			DestinationAddressSelector (str(addr1|addr2|anyAddr|notAddr1|notAddr2)): 
			Error (str(errAnyFrame|errBadCRC|errBadFrame|errGoodFrame)): 
			FrameSizeType (str(any|custom|jumbo|oversized|undersized)): 
			IsEnabled (bool): 
			PatternSelector (str(anyPattern|notPattern1|notPattern2|pattern1|pattern2)): 
			SourceAddressSelector (str(addr1|addr2|anyAddr|notAddr1|notAddr2)): 

		Returns:
			self: This instance with found uds data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
