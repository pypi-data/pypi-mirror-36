from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Layer23ProtocolRoutingFilter(Base):
	"""The Layer23ProtocolRoutingFilter class encapsulates a user managed layer23ProtocolRoutingFilter node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Layer23ProtocolRoutingFilter property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'layer23ProtocolRoutingFilter'

	def __init__(self, parent):
		super(Layer23ProtocolRoutingFilter, self).__init__(parent)

	@property
	def PortFilterIds(self):
		"""Ports that have been filtered.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])
		"""
		return self._get_attribute('portFilterIds')
	@PortFilterIds.setter
	def PortFilterIds(self, value):
		self._set_attribute('portFilterIds', value)

	@property
	def ProtocolFilterIds(self):
		"""Protocols that have been filtered.

		Returns:
			list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])
		"""
		return self._get_attribute('protocolFilterIds')
	@ProtocolFilterIds.setter
	def ProtocolFilterIds(self, value):
		self._set_attribute('protocolFilterIds', value)

	def add(self, PortFilterIds=None, ProtocolFilterIds=None):
		"""Adds a new layer23ProtocolRoutingFilter node on the server and retrieves it in this instance.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Ports that have been filtered.
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Protocols that have been filtered.

		Returns:
			self: This instance with all currently retrieved layer23ProtocolRoutingFilter data using find and the newly added layer23ProtocolRoutingFilter data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the layer23ProtocolRoutingFilter data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, PortFilterIds=None, ProtocolFilterIds=None):
		"""Finds and retrieves layer23ProtocolRoutingFilter data from the server.

		All named parameters support regex and can be used to selectively retrieve layer23ProtocolRoutingFilter data from the server.
		By default the find method takes no parameters and will retrieve all layer23ProtocolRoutingFilter data from the server.

		Args:
			PortFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availablePortFilter])): Ports that have been filtered.
			ProtocolFilterIds (list(str[None|/api/v1/sessions/1/ixnetwork/statistics?deepchild=availableProtocolFilter])): Protocols that have been filtered.

		Returns:
			self: This instance with found layer23ProtocolRoutingFilter data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
