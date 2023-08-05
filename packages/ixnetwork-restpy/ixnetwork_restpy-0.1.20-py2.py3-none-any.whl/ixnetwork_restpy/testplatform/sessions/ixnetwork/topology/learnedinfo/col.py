from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Col(Base):
	"""The Col class encapsulates a system managed col node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Col property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'col'

	def __init__(self, parent):
		super(Col, self).__init__(parent)

	@property
	def CellTable(self):
		"""An instance of the CellTable class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable.CellTable)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.celltable import CellTable
		return CellTable(self)

	@property
	def Row(self):
		"""An instance of the Row class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row.Row)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.learnedinfo.row import Row
		return Row(self)

	@property
	def Value(self):
		"""A learned information value

		Returns:
			str
		"""
		return self._get_attribute('value')

	def find(self, Value=None):
		"""Finds and retrieves col data from the server.

		All named parameters support regex and can be used to selectively retrieve col data from the server.
		By default the find method takes no parameters and will retrieve all col data from the server.

		Args:
			Value (str): A learned information value

		Returns:
			self: This instance with found col data from the server available through an iterator or index

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
