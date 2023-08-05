from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Stack(Base):
	"""The Stack class encapsulates a system managed stack node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Stack property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'stack'

	def __init__(self, parent):
		super(Stack, self).__init__(parent)

	@property
	def Field(self):
		"""An instance of the Field class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.field.field.Field)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.traffic.trafficitem.configelement.stack.field.field import Field
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
		"""Finds and retrieves stack data from the server.

		All named parameters support regex and can be used to selectively retrieve stack data from the server.
		By default the find method takes no parameters and will retrieve all stack data from the server.

		Args:
			DisplayName (str): 
			StackTypeId (str): 
			TemplateName (str): 

		Returns:
			self: This instance with found stack data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def Append(self, Arg2):
		"""Executes the append operation on the server.

		Append a protocol template after the specified stack object reference.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference.

		Returns:
			str: This exec returns an object reference to the newly appended stack item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Append', payload=locals(), response_object=None)

	def AppendProtocol(self, Arg2):
		"""Executes the appendProtocol operation on the server.

		Append a protocol template after the specified stack object reference.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference.

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack): This exec returns an object reference to the newly appended stack item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('AppendProtocol', payload=locals(), response_object=None)

	def Insert(self, Arg2):
		"""Executes the insert operation on the server.

		Insert a protocol template before the specified stack object reference.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference

		Returns:
			str: This exec returns an object reference to the newly inserted stack item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Insert', payload=locals(), response_object=None)

	def InsertProtocol(self, Arg2):
		"""Executes the insertProtocol operation on the server.

		Insert a protocol template before the specified stack object reference.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=protocolTemplate)): A valid /traffic/protocolTemplate object reference

		Returns:
			str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack): This exec returns an object reference to the newly inserted stack item.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('InsertProtocol', payload=locals(), response_object=None)

	def Remove(self):
		"""Executes the remove operation on the server.

		Delete the specified stack object reference.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/traffic?deepchild=stack)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Remove', payload=locals(), response_object=None)
