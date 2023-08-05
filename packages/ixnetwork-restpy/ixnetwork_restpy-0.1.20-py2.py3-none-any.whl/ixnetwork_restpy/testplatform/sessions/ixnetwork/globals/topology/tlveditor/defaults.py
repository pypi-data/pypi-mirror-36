from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Defaults(Base):
	"""The Defaults class encapsulates a system managed defaults node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Defaults property from a parent instance.
	The internal properties list will be empty when the property is accessed and is populated from the server by using the find method.
	"""

	_SDM_NAME = 'defaults'

	def __init__(self, parent):
		super(Defaults, self).__init__(parent)

	@property
	def Template(self):
		"""An instance of the Template class.

		Returns:
			obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template.Template)

		Raises:
			NotFoundError: The requested resource does not exist on the server
			ServerError: The server has encountered an uncategorized error condition
		"""
		from ixnetwork_restpy.testplatform.sessions.ixnetwork.globals.topology.tlveditor.template import Template
		return Template(self)

	def find(self):
		"""Finds and retrieves defaults data from the server.

		All named parameters support regex and can be used to selectively retrieve defaults data from the server.
		By default the find method takes no parameters and will retrieve all defaults data from the server.

		Returns:
			self: This instance with found defaults data from the server available through an iterator or index

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
