from datetime import datetime

def get_gh_formatted_date(dt):
	""" get the date as per github datetime format """
	return get_formatted_date(dt, dt_format='%Y-%m-%dT%H:%M:%SZ',
		conversion_format='%Y-%m-%dT%H:%M:%SZ')

def get_formatted_date(dt, dt_format='%Y-%m-%d %H:%M:%S',
	conversion_format='%Y-%m-%d %H:%M:%S'):
	""" format datetime """
	if not dt:
		dt = datetime.now()
	elif isinstance(dt, str):
		dt = datetime.strptime(dt, conversion_format)

	return dt.strftime(dt_format) 