from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class FlowAggrMatchTemplate(Base):
	"""The FlowAggrMatchTemplate class encapsulates a required flowAggrMatchTemplate node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the FlowAggrMatchTemplate property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'flowAggrMatchTemplate'

	def __init__(self, parent):
		super(FlowAggrMatchTemplate, self).__init__(parent)

	@property
	def MatchTemplate(self):
		"""An instance of the MatchTemplate class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchtemplate.MatchTemplate)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.matchtemplate import MatchTemplate
		return MatchTemplate(self)

	@property
	def Predefined(self):
		"""An instance of the Predefined class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.predefined.Predefined)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.openflowchannel.predefined import Predefined
		return Predefined(self)

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
