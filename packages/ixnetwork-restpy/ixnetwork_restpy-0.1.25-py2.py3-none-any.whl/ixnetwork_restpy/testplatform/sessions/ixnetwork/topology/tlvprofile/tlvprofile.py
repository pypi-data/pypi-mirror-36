from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TlvProfile(Base):
	"""The TlvProfile class encapsulates a system managed tlvProfile node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TlvProfile property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'tlvProfile'

	def __init__(self, parent):
		super(TlvProfile, self).__init__(parent)

	@property
	def DefaultTlv(self):
		"""An instance of the DefaultTlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv.DefaultTlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.defaulttlv import DefaultTlv
		return DefaultTlv(self)

	@property
	def Tlv(self):
		"""An instance of the Tlv class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv.Tlv)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.tlvprofile.tlv import Tlv
		return Tlv(self)

	def find(self):
		"""Finds and retrieves tlvProfile data from the server.

		All named parameters support regex and can be used to selectively retrieve tlvProfile data from the server.
		By default the find method takes no parameters and will retrieve all tlvProfile data from the server.

		Returns:
			self: This instance with found tlvProfile data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def CopyTlv(self, Arg2):
		"""Executes the copyTlv operation on the server.

		Copy a template tlv to a topology tlv profile

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/topology)): The method internally set Arg1 to the current href for this instance
			Arg2 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=topology)): An object reference to a source template tlv

		Returns:
			str(None): An object reference to the newly created topology tlv as a result of the copy operation

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('CopyTlv', payload=locals(), response_object=None)
