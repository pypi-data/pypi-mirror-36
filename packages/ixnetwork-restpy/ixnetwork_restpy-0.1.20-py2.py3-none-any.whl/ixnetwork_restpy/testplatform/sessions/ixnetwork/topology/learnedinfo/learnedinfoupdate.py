from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LearnedInfoUpdate(Base):
	"""The LearnedInfoUpdate class encapsulates a system managed learnedInfoUpdate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LearnedInfoUpdate property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'learnedInfoUpdate'

	def __init__(self, parent):
		super(LearnedInfoUpdate, self).__init__(parent)

	@property
	def PceBasicRsvpSyncLspUpdateParams(self):
		"""An instance of the PceBasicRsvpSyncLspUpdateParams class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicrsvpsynclspupdateparams.PceBasicRsvpSyncLspUpdateParams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicrsvpsynclspupdateparams import PceBasicRsvpSyncLspUpdateParams
		return PceBasicRsvpSyncLspUpdateParams(self)

	@property
	def PceBasicSrSyncLspUpdateParams(self):
		"""An instance of the PceBasicSrSyncLspUpdateParams class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicsrsynclspupdateparams.PceBasicSrSyncLspUpdateParams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcebasicsrsynclspupdateparams import PceBasicSrSyncLspUpdateParams
		return PceBasicSrSyncLspUpdateParams(self)

	@property
	def PceDetailedRsvpSyncLspUpdateParams(self):
		"""An instance of the PceDetailedRsvpSyncLspUpdateParams class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedrsvpsynclspupdateparams.PceDetailedRsvpSyncLspUpdateParams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedrsvpsynclspupdateparams import PceDetailedRsvpSyncLspUpdateParams
		return PceDetailedRsvpSyncLspUpdateParams(self)

	@property
	def PceDetailedSrSyncLspUpdateParams(self):
		"""An instance of the PceDetailedSrSyncLspUpdateParams class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedsrsynclspupdateparams.PceDetailedSrSyncLspUpdateParams)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.pcedetailedsrsynclspupdateparams import PceDetailedSrSyncLspUpdateParams
		return PceDetailedSrSyncLspUpdateParams(self)

	def find(self):
		"""Finds and retrieves learnedInfoUpdate data from the server.

		All named parameters support regex and can be used to selectively retrieve learnedInfoUpdate data from the server.
		By default the find method takes no parameters and will retrieve all learnedInfoUpdate data from the server.

		Returns:
			self: This instance with found learnedInfoUpdate data from the server available through an iterator or index

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
