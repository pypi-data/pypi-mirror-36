from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class TransmissionControl(Base):
	"""The TransmissionControl class encapsulates a required transmissionControl node in the ixnetwork hierarchy.

	An instance of the class can be obtained by accessing the TransmissionControl property from a parent instance.
	The internal properties list will contain one and only one set of properties which is populated when the property is accessed.
	"""

	_SDM_NAME = 'transmissionControl'

	def __init__(self, parent):
		super(TransmissionControl, self).__init__(parent)

	@property
	def BurstPacketCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('burstPacketCount')
	@BurstPacketCount.setter
	def BurstPacketCount(self, value):
		self._set_attribute('burstPacketCount', value)

	@property
	def Duration(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('duration')
	@Duration.setter
	def Duration(self, value):
		self._set_attribute('duration', value)

	@property
	def EnableInterBurstGap(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableInterBurstGap')
	@EnableInterBurstGap.setter
	def EnableInterBurstGap(self, value):
		self._set_attribute('enableInterBurstGap', value)

	@property
	def EnableInterStreamGap(self):
		"""

		Returns:
			bool
		"""
		return self._get_attribute('enableInterStreamGap')
	@EnableInterStreamGap.setter
	def EnableInterStreamGap(self, value):
		self._set_attribute('enableInterStreamGap', value)

	@property
	def FrameCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('frameCount')
	@FrameCount.setter
	def FrameCount(self, value):
		self._set_attribute('frameCount', value)

	@property
	def InterBurstGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interBurstGap')
	@InterBurstGap.setter
	def InterBurstGap(self, value):
		self._set_attribute('interBurstGap', value)

	@property
	def InterBurstGapUnits(self):
		"""

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('interBurstGapUnits')
	@InterBurstGapUnits.setter
	def InterBurstGapUnits(self, value):
		self._set_attribute('interBurstGapUnits', value)

	@property
	def InterStreamGap(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('interStreamGap')
	@InterStreamGap.setter
	def InterStreamGap(self, value):
		self._set_attribute('interStreamGap', value)

	@property
	def IterationCount(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('iterationCount')
	@IterationCount.setter
	def IterationCount(self, value):
		self._set_attribute('iterationCount', value)

	@property
	def MinGapBytes(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('minGapBytes')
	@MinGapBytes.setter
	def MinGapBytes(self, value):
		self._set_attribute('minGapBytes', value)

	@property
	def RepeatBurst(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('repeatBurst')
	@RepeatBurst.setter
	def RepeatBurst(self, value):
		self._set_attribute('repeatBurst', value)

	@property
	def StartDelay(self):
		"""

		Returns:
			number
		"""
		return self._get_attribute('startDelay')
	@StartDelay.setter
	def StartDelay(self, value):
		self._set_attribute('startDelay', value)

	@property
	def StartDelayUnits(self):
		"""

		Returns:
			str(bytes|nanoseconds)
		"""
		return self._get_attribute('startDelayUnits')
	@StartDelayUnits.setter
	def StartDelayUnits(self, value):
		self._set_attribute('startDelayUnits', value)

	@property
	def Type(self):
		"""

		Returns:
			str(auto|continuous|custom|fixedDuration|fixedFrameCount|fixedIterationCount)
		"""
		return self._get_attribute('type')
	@Type.setter
	def Type(self, value):
		self._set_attribute('type', value)
