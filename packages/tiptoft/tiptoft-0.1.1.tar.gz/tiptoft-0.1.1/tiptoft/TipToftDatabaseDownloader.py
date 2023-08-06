import logging
import os
from tiptoft.RefGenesGetter import RefGenesGetter

class TipToftDatabaseDownloader:
	def __init__(self,options):
		self.logger = logging.getLogger(__name__)
		self.output_prefix = options.output_prefix
		self.verbose = options.verbose
		
		if self.verbose:
			self.logger.setLevel(logging.DEBUG)
		else:
			self.logger.setLevel(logging.ERROR)
			
	def run(self):
		refgenes  = RefGenesGetter(verbose = self.verbose)
		
		if self.output_prefix:
			refgenes.run( self.output_prefix)
		else:
			self.logger.error("Please check the input parameters")
