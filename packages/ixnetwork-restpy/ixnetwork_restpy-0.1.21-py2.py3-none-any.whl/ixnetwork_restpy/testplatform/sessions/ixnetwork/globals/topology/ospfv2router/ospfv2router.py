from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Ospfv2Router(Base):
	"""The Ospfv2Router class encapsulates a system managed ospfv2Router node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Ospfv2Router property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'ospfv2Router'

	def __init__(self, parent):
		super(Ospfv2Router, self).__init__(parent)

	@property
	def StartRate(self):
		"""An instance of the StartRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.startrate.startrate.StartRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.startrate.startrate import StartRate
		return StartRate(self)._select()

	@property
	def StopRate(self):
		"""An instance of the StopRate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.stoprate.stoprate.StopRate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.ospfv2router.stoprate.stoprate import StopRate
		return StopRate(self)._select()

	@property
	def BierMplsEncapSubTlvType(self):
		"""BIER MPLS Encapsulation Sub-TLV

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierMplsEncapSubTlvType')

	@property
	def BierSubTlvType(self):
		"""BIER Sub-TLV Type

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('bierSubTlvType')

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
	def EnableDrBdr(self):
		"""Enable DR/BDR

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('enableDrBdr')

	@property
	def FloodLsUpdatesPerInterval(self):
		"""Flood Link State Updates per Interval

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('floodLsUpdatesPerInterval')

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
	def RateControlInterval(self):
		"""Rate Control Interval (ms)

		Returns:
			obj(ixnetwork_restpy.multivalue.Multivalue)
		"""
		return self._get_attribute('rateControlInterval')

	@property
	def RowNames(self):
		"""Name of rows

		Returns:
			list(str)
		"""
		return self._get_attribute('rowNames')

	def find(self, Count=None, DescriptiveName=None, Name=None, RowNames=None):
		"""Finds and retrieves ospfv2Router data from the server.

		All named parameters support regex and can be used to selectively retrieve ospfv2Router data from the server.
		By default the find method takes no parameters and will retrieve all ospfv2Router data from the server.

		Args:
			Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group
			DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but maybe offers more context
			Name (str): Name of NGPF element, guaranteed to be unique in Scenario
			RowNames (list(str)): Name of rows

		Returns:
			self: This instance with found ospfv2Router data from the server available through an iterator or index

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
