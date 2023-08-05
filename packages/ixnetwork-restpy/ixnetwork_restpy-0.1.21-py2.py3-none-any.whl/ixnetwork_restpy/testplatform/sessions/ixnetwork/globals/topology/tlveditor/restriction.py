from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Restriction(Base):
	"""The Restriction class encapsulates a user managed restriction node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Restriction property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server using the find method.
	The internal properties list can be managed by the user by using the add and remove methods.
	"""

	_SDM_NAME = 'restriction'

	def __init__(self, parent):
		super(Restriction, self).__init__(parent)

	@property
	def Enum(self):
		"""Internal enumeration type to be used as value options

		Returns:
			str
		"""
		return self._get_attribute('enum')
	@Enum.setter
	def Enum(self, value):
		self._set_attribute('enum', value)

	@property
	def SingleValue(self):
		"""Restricts the field to single value pattern without overlays

		Returns:
			bool
		"""
		return self._get_attribute('singleValue')
	@SingleValue.setter
	def SingleValue(self, value):
		self._set_attribute('singleValue', value)

	def add(self, Enum=None, SingleValue=None):
		"""Adds a new restriction node on the server and retrieves it in this instance.

		Args:
			Enum (str): Internal enumeration type to be used as value options
			SingleValue (bool): Restricts the field to single value pattern without overlays

		Returns:
			self: This instance with all currently retrieved restriction data using find and the newly added restriction data available through an iterator or index

		Raises:
			ServerError: The server has encountered an uncategorized error condition
		"""
		return self._create(locals())

	def remove(self):
		"""Deletes all the restriction data in this instance from server.

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		self._delete()

	def find(self, Enum=None, SingleValue=None):
		"""Finds and retrieves restriction data from the server.

		All named parameters support regex and can be used to selectively retrieve restriction data from the server.
		By default the find method takes no parameters and will retrieve all restriction data from the server.

		Args:
			Enum (str): Internal enumeration type to be used as value options
			SingleValue (bool): Restricts the field to single value pattern without overlays

		Returns:
			self: This instance with found restriction data from the server available through an iterator or index

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
