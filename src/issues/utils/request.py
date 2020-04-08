import requests
from django.conf import settings

def before_request():
	""" add session_id in the request body """
	payload = {}
	headers = {
		'Authorization': 'token {0}'.format(settings.GH_ACCESS_TOKEN)
	}
	return payload, headers

def github_request(uri, method='GET', payload={},
	error_msg='Internal server error', allow_before_request=True):
	""" common method to send the python requests """
	response = None
	if not uri:
		return

	if allow_before_request:
		args, headers = before_request()

	payload.update(args)

	base_url = "https://api.github.com"
	url = f"{base_url}/{uri}"

	try:
		args = {
			"headers": headers,
			"data" if method != "GET" else "params": payload
		}
		response = requests.request(method, url, **args)
		if response.status_code == 200:
			return response.json() or {}
		else:
			print(response.status_code, response.reason, "error")
			return None
	except Exception as e:
		print(e)
		return None
