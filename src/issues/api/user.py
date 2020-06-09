from issues.models import GitHubUser
from issues.utils.request import github_request

def fetch_user(github_username=None):
	""" fetch user details from github abd store it in db  """
	uri = 'user' if not github_username else f'users/{github_username}'
	user_info = github_request(uri)

	if not user_info:
		return None

	return get_or_create_user(user_info, is_superuser=True)


def get_or_create_user(user_info, is_superuser=False, is_staff=True):
	""" check if user is already exists, if not then create one """
	user = None
	if not user_info:
		return user

	github_username = user_info.get('login', None)
	if not github_username:
		return None

	full_name = user_info.get('name', '')
	email = user_info.get('email', None)
	if not email:
		email = '{0}@example.com'.format(full_name.lower().replace(' ', '.') \
			if full_name else github_username)

	# check if user already exists
	user = GitHubUser.objects.filter(username=github_username,
		github_username=github_username)

	to_update = {
		"email": email,
		"username": github_username,
		"github_username": github_username
	}

	if full_name:
		to_update.update({
			"first_name": full_name.split(' ')[0],
			"last_name": full_name.split(' ')[-1],
		})


	if not user.exists():
		user = GitHubUser()
		to_update = {
			"is_staff": is_staff,
			"is_superuser": is_superuser
		}
	user = user.first()

	for key, val in to_update.items():
		setattr(user, key, val)

	user.set_password(github_username)
	user.save()

	return user
