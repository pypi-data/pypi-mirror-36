from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class ProtocolTemplate(Base):
	"""The ProtocolTemplate class encapsulates a system managed protocolTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the ProtocolTemplate property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'protocolTemplate'

	def __init__(self, parent):
		super(ProtocolTemplate, self).__init__(parent)

	@property
	def Field(self):
		"""An instance of the Field class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field.Field)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.protocoltemplate.field.field import Field
		return Field(self)

	@property
	def DisplayName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('displayName')

	@property
	def StackTypeId(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('stackTypeId')

	@property
	def TemplateName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('templateName')

	def find(self, DisplayName=None, StackTypeId=None, TemplateName=None):
		"""Finds and retrieves protocolTemplate data from the server.

		All named parameters support regex and can be used to selectively retrieve protocolTemplate data from the server.
		By default the find method takes no parameters and will retrieve all protocolTemplate data from the server.

		Args:
			DisplayName (str): 
			StackTypeId (str): 
			TemplateName (str): 

		Returns:
			self: This instance with found protocolTemplate data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
