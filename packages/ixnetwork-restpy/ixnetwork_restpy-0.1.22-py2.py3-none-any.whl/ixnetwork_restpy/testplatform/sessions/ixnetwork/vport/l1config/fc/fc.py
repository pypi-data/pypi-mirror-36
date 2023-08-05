from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class Fc(Base):
	"""The Fc class encapsulates a required fc node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the Fc property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'fc'

	def __init__(self, parent):
		super(Fc, self).__init__(parent)

	@property
	def CreditStarvationValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('creditStarvationValue')
	@CreditStarvationValue.setter
	def CreditStarvationValue(self, value):
		self._set_attribute('creditStarvationValue', value)

	@property
	def EnableEmissionLoweringProtocol(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableEmissionLoweringProtocol')
	@EnableEmissionLoweringProtocol.setter
	def EnableEmissionLoweringProtocol(self, value):
		self._set_attribute('enableEmissionLoweringProtocol', value)

	@property
	def EnablePPM(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enablePPM')
	@EnablePPM.setter
	def EnablePPM(self, value):
		self._set_attribute('enablePPM', value)

	@property
	def FixedDelayValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('fixedDelayValue')
	@FixedDelayValue.setter
	def FixedDelayValue(self, value):
		self._set_attribute('fixedDelayValue', value)

	@property
	def ForceErrors(self):
		"""

		Returns:
			str(noErrors|noRRDY|noRRDYEvery)
		"""
		return self._get_attribute('forceErrors')
	@ForceErrors.setter
	def ForceErrors(self, value):
		self._set_attribute('forceErrors', value)

	@property
	def Loopback(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('loopback')
	@Loopback.setter
	def Loopback(self, value):
		self._set_attribute('loopback', value)

	@property
	def MaxDelayForRandomValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('maxDelayForRandomValue')
	@MaxDelayForRandomValue.setter
	def MaxDelayForRandomValue(self, value):
		self._set_attribute('maxDelayForRandomValue', value)

	@property
	def MinDelayForRandomValue(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minDelayForRandomValue')
	@MinDelayForRandomValue.setter
	def MinDelayForRandomValue(self, value):
		self._set_attribute('minDelayForRandomValue', value)

	@property
	def NoRRDYAfter(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('noRRDYAfter')
	@NoRRDYAfter.setter
	def NoRRDYAfter(self, value):
		self._set_attribute('noRRDYAfter', value)

	@property
	def Ppm(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('ppm')
	@Ppm.setter
	def Ppm(self, value):
		self._set_attribute('ppm', value)

	@property
	def RrdyResponseDelays(self):
		"""

		Returns:
			str(creditStarvation|fixedDelay|noDelay|randomDelay)
		"""
		return self._get_attribute('rrdyResponseDelays')
	@RrdyResponseDelays.setter
	def RrdyResponseDelays(self, value):
		self._set_attribute('rrdyResponseDelays', value)

	@property
	def Speed(self):
		"""

		Returns:
			str(speed2000|speed4000|speed8000)
		"""
		return self._get_attribute('speed')
	@Speed.setter
	def Speed(self, value):
		self._set_attribute('speed', value)

	@property
	def TxIgnoreAvailableCredits(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreAvailableCredits')
	@TxIgnoreAvailableCredits.setter
	def TxIgnoreAvailableCredits(self, value):
		self._set_attribute('txIgnoreAvailableCredits', value)

	@property
	def TxIgnoreRxLinkFaults(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('txIgnoreRxLinkFaults')
	@TxIgnoreRxLinkFaults.setter
	def TxIgnoreRxLinkFaults(self, value):
		self._set_attribute('txIgnoreRxLinkFaults', value)
