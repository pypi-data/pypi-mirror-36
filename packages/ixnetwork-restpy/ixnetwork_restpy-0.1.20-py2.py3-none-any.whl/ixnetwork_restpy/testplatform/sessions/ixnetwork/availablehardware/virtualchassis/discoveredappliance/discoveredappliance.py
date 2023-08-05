from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class DiscoveredAppliance(Base):
	"""The DiscoveredAppliance class encapsulates a system managed discoveredAppliance node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the DiscoveredAppliance property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'discoveredAppliance'

	def __init__(self, parent):
		super(DiscoveredAppliance, self).__init__(parent)

	@property
	def DiscoveredInterface(self):
		"""An instance of the DiscoveredInterface class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.discoveredappliance.discoveredinterface.discoveredinterface.DiscoveredInterface)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.availablehardware.virtualchassis.discoveredappliance.discoveredinterface.discoveredinterface import DiscoveredInterface
		return DiscoveredInterface(self)

	@property
	def ApplianceName(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('applianceName')

	@property
	def ApplianceType(self):
		"""

		Returns:
			str(qemu|vCenter|vmware)
		"""
		return self._get_attribute('applianceType')

	@property
	def InterfacesNumber(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interfacesNumber')

	@property
	def ManagementIp(self):
		"""

		Returns:
			str
		"""
		return self._get_attribute('managementIp')

	def find(self, ApplianceName=None, ApplianceType=None, InterfacesNumber=None, ManagementIp=None):
		"""Finds and retrieves discoveredAppliance data from the server.

		All named parameters support regex and can be used to selectively retrieve discoveredAppliance data from the server.
		By default the find method takes no parameters and will retrieve all discoveredAppliance data from the server.

		Args:
			ApplianceName (str): 
			ApplianceType (str(qemu|vCenter|vmware)): 
			InterfacesNumber (number): 
			ManagementIp (str): 

		Returns:
			self: This instance with found discoveredAppliance data from the server available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._select(locals())
