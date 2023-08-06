from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class LinkOam(Base):
	"""The LinkOam class encapsulates a required linkOam node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the LinkOam property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'linkOam'

	def __init__(self, parent):
		super(LinkOam, self).__init__(parent)

	@property
	def Link(self):
		"""An instance of the Link class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.link.Link)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.linkoam.link.link import Link
		return Link(self)

	@property
	def Enabled(self):
		"""If true, the Link OAM protocol is enabled.

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def RunningState(self):
		"""The current runnings state of Link OAM.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def Start(self):
		"""Executes the start operation on the server.

		Starts the Link OAM protocol.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=linkOam)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the Link OAM protocol

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=linkOam)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
