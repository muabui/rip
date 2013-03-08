#!/usr/bin/python

from basesite import basesite

"""
	Downloads imagefap albums
"""
class imagefap(basesite):
	"""
		Ensure URL is relevant to this ripper.
		Return 'sanitized' URL (if needed).
	"""
	def sanitize_url(self, url):
		if not 'imagefap.com/' in url: 
			raise Exception('')
		if not 'imagefap.com/pictures/' in url:
			raise Exception("Required '/pictures/' not found")
		if '?' in url: url = url[:url.find('?')]
		return '%s?view=2' % url

	""" Discover directory path based on URL """
	def get_dir(self, url):
		u = self.url
		u = u[:u.find('?')]
		while u.endswith('/'): u = u[:-1]
		name = u[u.rfind('/', u.rfind('/') - 2) + 1:]
		name = name.replace('/', '_')
		return 'imagefap_%s' % name

	def download(self):
		# Get album source
		self.log('loading album...')
		r = self.web.get(self.url)
		# Get images
		links = self.web.between(r, 'x.fap.to/images/thumb/', '"')
		for index, link in enumerate(links):
			if index == 0: continue # Skip first URL (user image?)
			link = 'http://fap.to/images/full/%s' % link
			# Download every image
			# Uses superclass threaded download method
			self.download_image(link, index, total=len(links) - 1) 
		self.wait_for_threads()
