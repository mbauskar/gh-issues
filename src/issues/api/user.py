from issues.models import GitHubUser
from issues.utils.request import github_request

def get_user(github_username=None):
	""" fetch user details from github abd store it in db  """
	uri = 'user' if not github_username else f'users/{github_username}'
	user_info = github_request(uri)

	if not user_info:
		return None

	# check if user already exists
	github_username = user_info.get('login', None)
	if not github_username:
		return None


	user = None
	full_name = user_info.get('name', '')
	first_name = full_name.split(' ')[0]
	last_name = full_name.split(' ')[-1]
	email = user_info.get('email', None)
	if not email:
		email = '{0}@example.com'.format(full_name.lower().replace(' ', ','))

	to_udpate = {
		"email": email,
		"last_name": last_name,
		"first_name": first_name,
		"username": github_username,
		"github_username": github_username
	}

	user = GitHubUser.objects.filter(username=github_username,
		github_username=github_username)

	user = GitHubUser() if not user.exists() else user.first()
	for key, val in to_udpate.items():
		setattr(user, key, val)

	user.set_password(github_username)
	user.save()

	return user
