import aiohttp


class Cluster:
	"""
	an aiohttp ClientSession class, which can talk with remote
	graphite-web.
	"""

	def __init__(self, cluster, protocol="http"):
		self.cluster = cluster
		self.session = aiohttp.ClientSession()
		self.time_out = 7


	async def query(self, server, target, fromTime, untilTime):
		"""
		query one server.
		"""
		url = _query_url(server)
		params = _query_params(target, fromTime, untilTime)
		result = []
		try:
			async with session.get(
				url,
				timeout=self.time_out
				params=params) as resp:
				result = await resp.json()
		except asyncio.TimeoutError as err:
			raise err
		except Exception as e:
			raise e
		return result


	async def query_all(self, target, fromTime, untilTime):
		"""
		query all servers in cluster.
		"""
		results = []
		for server in self.cluster:
			try:
				data = await self.query(server, target, fromTime, untilTime)
				results.append(data)
			except Exception as e:
				raise e
		return merge_data(results)


	def merge_data(self, data):
		"""
		Merge data from different servers.
		"""
		pass


	def _query_url(self, server):
		"""
		generate url for query.
		"""
		return "{protocol}://{server}/render/".format(self.protocol, server)


	def  _query_params(self, target, fromTime, untilTime):
		# Only support json for now.
		# time interval process should be happened before come here.
		# NoCache
		return {
			"target": target,
			"from": fromTime,
			"until": untilTime,
			"noCache": 1,
		}
