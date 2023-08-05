from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Row(Base):
	"""The Row class encapsulates a system managed row node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Row property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'row'

	def __init__(self, parent):
		super(Row, self).__init__(parent)

	@property
	def Value(self):
		"""A learned information value

		Returns:
			str
		"""
		return self._get_attribute('value')

	def find(self, Value=None):
		"""Finds and retrieves row data from the server.

		All named parameters support regex and can be used to selectively retrieve row data from the server.
		By default the find method takes no parameters and will retrieve all row data from the server.

		Args:
			Value (str): A learned information value

		Returns:
			self: This instance with found row data from the server available through an iterator or index

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
