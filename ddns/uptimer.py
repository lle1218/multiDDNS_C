#!/usr/bim/env python
# _*_ coding: utf-8 _*_

import pdb
import threading

class RepeatableTimer(object):
	def __init__(self, interval, function, args=[]):
		self.interval = interval
		self.function = function
		self.args = args

	def start(self):
		self.stop()
		self._timer = threading.Timer(self.interval, self._run)
#		self._timer.setDaemon(True)
		self._timer.setDaemon(False)
		self._timer.start()

	def restart(self):
		self.start()


	def stop(self):
		if self.__dict__.has_key("_timer"):
			self._timer.cancel()
			del self._timer

	def _run(self):
		try:
			self.function(self.args)
		except:
			pass
		self.restart()

