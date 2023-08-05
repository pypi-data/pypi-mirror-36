from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class PcepEroSubObjectsList(Base):
	"""The PcepEroSubObjectsList class encapsulates a system managed pcepEroSubObjectsList node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the PcepEroSubObjectsList property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'pcepEroSubObjectsList'

	def __init__(self, parent):
		super(PcepEroSubObjectsList, self).__init__(parent)

	@property
	def Active(self):
		"""Controls whether the ERO sub-object will be sent in the PCInitiate message.

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
	def Bos(self):
		"""This bit is set to true for the last entry in the label stack i.e., for the bottom of the stack, and false for all other label stack entries. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bos')

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
	def FBit(self):
		"""A Flag which is used to carry additional information pertaining to SID. When this bit is set, the NAI value in the subobject body is null.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('fBit')

	@property
	def Ipv4NodeId(self):
		"""IPv4 Node ID is specified as an IPv4 address. This control can be configured if NAI Type is set to IPv4 Node ID and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4NodeId')

	@property
	def Ipv4Prefix(self):
		"""IPv4 Prefix is specified as an IPv4 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv4Prefix')

	@property
	def Ipv6NodeId(self):
		"""IPv6 Node ID is specified as an IPv6 address. This control can be configured if NAI Type is set to IPv6 Node ID and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6NodeId')

	@property
	def Ipv6Prefix(self):
		"""IPv6 Prefix is specified as an IPv6 address.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ipv6Prefix')

	@property
	def LocalInterfaceId(self):
		"""This is the Local Interface ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localInterfaceId')

	@property
	def LocalIpv4Address(self):
		"""This Control can be configured if NAI Type is set to IPv4 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv4Address')

	@property
	def LocalIpv6Address(self):
		"""This Control can be configured if NAI Type is set to IPv6 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localIpv6Address')

	@property
	def LocalNodeId(self):
		"""This is the Local Node ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('localNodeId')

	@property
	def LooseHop(self):
		"""Indicates if user wants to represent a loose-hop sub object in the LSP

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('looseHop')

	@property
	def MplsLabel(self):
		"""This control will be editable if the SID Type is set to either 20bit or 32bit MPLS-Label. This field will take the 20bit value of the MPLS-Label

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('mplsLabel')

	@property
	def NaiType(self):
		"""NAI (Node or Adjacency Identifier) contains the NAI associated with the SID. Depending on the value of SID Type, the NAI can have different formats such as, Not Applicable IPv4 Node ID IPv6 Node ID IPv4 Adjacency IPv6 Adjacency Unnumbered Adjacency with IPv4 NodeIDs

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('naiType')

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
	def RemoteInterfaceId(self):
		"""This is the Remote Interface ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteInterfaceId')

	@property
	def RemoteIpv4Address(self):
		"""This Control can be configured if NAI Type is set to IPv4 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv4Address')

	@property
	def RemoteIpv6Address(self):
		"""This Control can be configured if NAI Type is set to IPv6 Adjacency and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteIpv6Address')

	@property
	def RemoteNodeId(self):
		"""This is the Remote Node ID of the Unnumbered Adjacency with IPv4 NodeIDs which is specified as a pair of Node ID / Interface ID tuples. This Control can be configured if NAI Type is set to Unnumbered Adjacency with IPv4 NodeIDs and F bit is disabled.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('remoteNodeId')

	@property
	def Sid(self):
		"""SID is the Segment Identifier

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sid')

	@property
	def SidType(self):
		"""Using the Segment Identifier Type control user can configure whether to include SID or not and if included what is its type. Types are as follows: Null SID 20bit MPLS Label 32bit MPLS Label. If it is Null then S bit is set in the packet. Default value is 20bit MPLS Label.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('sidType')

	@property
	def SubObjectType(self):
		"""Using the Sub Object Type control user can configure which sub object needs to be included from the following options: Not Applicable IPv4 Prefix IPv6 Prefix AS Number.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('subObjectType')

	@property
	def Tc(self):
		"""This field is used to carry traffic class information. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('tc')

	@property
	def Ttl(self):
		"""This field is used to encode a time-to-live value. This control will be editable only if SID Type is MPLS Label 32bit.

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('ttl')

	def find(self, Count=None, DescriptiveName=None, Name=None):
		"""Finds and retrieves pcepEroSubObjectsList data from the server.

		All named parameters support regex and can be used to selectively retrieve pcepEroSubObjectsList data from the server.
		By default the find method takes no parameters and will retrieve all pcepEroSubObjectsList data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario

		Returns:
			self: This instance with found pcepEroSubObjectsList data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())

	def FetchAndUpdateConfigFromCloud(self, Mode):
		"""Executes the fetchAndUpdateConfigFromCloud operation on the server.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/globals?deepchild=*|/api/v1/sessions/1/ixnetwork/topology?deepchild=*)): The method internally set Arg1 to the current href for this instance
			Mode (str): 

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('FetchAndUpdateConfigFromCloud', payload=locals(), response_object=None)
