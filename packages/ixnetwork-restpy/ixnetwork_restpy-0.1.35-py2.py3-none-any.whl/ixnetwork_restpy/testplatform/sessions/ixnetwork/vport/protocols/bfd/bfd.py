from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Bfd(Base):
	"""The Bfd class encapsulates a required bfd node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Bfd property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'bfd'

	def __init__(self, parent):
		super(Bfd, self).__init__(parent)

	@property
	def Router(self):
		"""An instance of the Router class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bfd.router.router.Router)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.vport.protocols.bfd.router.router import Router
		return Router(self)

	@property
	def Enabled(self):
		"""Enables or disables the use of this emulated BFD router in the emulated BFD network. (default = disabled)

		Returns:
			bool
		"""
		return self._get_attribute('enabled')
	@Enabled.setter
	def Enabled(self, value):
		self._set_attribute('enabled', value)

	@property
	def IntervalValue(self):
		"""Interval Value

		Returns:
			number
		"""
		return self._get_attribute('intervalValue')
	@IntervalValue.setter
	def IntervalValue(self, value):
		self._set_attribute('intervalValue', value)

	@property
	def PacketsPerInterval(self):
		"""Number of BFD control packets per interval.

		Returns:
			number
		"""
		return self._get_attribute('packetsPerInterval')
	@PacketsPerInterval.setter
	def PacketsPerInterval(self, value):
		self._set_attribute('packetsPerInterval', value)

	@property
	def RunningState(self):
		"""The current running state of the BFD protocol.

		Returns:
			str(unknown|stopped|stopping|starting|started)
		"""
		return self._get_attribute('runningState')

	def Start(self):
		"""Executes the start operation on the server.

		Starts the BFD protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bfd)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Start', payload=locals(), response_object=None)

	def Stop(self):
		"""Executes the stop operation on the server.

		Stops the BFD protocol on a port or group of ports.

		Args:
			Arg1 (str(None|/api/v1/sessions/1/ixnetwork/vport?deepchild=bfd)): The method internally set Arg1 to the current href for this instance

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		Arg1 = self.href
		return self._execute('Stop', payload=locals(), response_object=None)
