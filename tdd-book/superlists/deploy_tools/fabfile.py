import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/jdodson3106/tdd-practice.git'

def depoloy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	run(f'mkdir -p {site_folder}')
	with cd(site_folder):
		_get_latest_source()
		_update_virtualenv()
		_create_or_update_dotenv()
		_update_static_files()
		_update_database()


def _get_latest_source():
	# check the .git hidden folder to see if the repo has already been cloned
	if exists('.git'):
		run('git fetch')  # git fetch all the latest commits from the repo
	else:
		run(f'git clone {REPO_URL} .') # if the repo is not abailable then we clone the a fresh source tree from the github repo

	# fabric's local command here will get the id of the current commit
	# from the git log invocation so that the server gets whatever code is 
	# currently checked out on the machine
	current_commit = local("git log -n 1 --format=%H", capture=True)  
	run(f'git reset --hard {current_commit}')  # hard reset to git rid of any other changes in code repo currently on the server

def _update_virtualenv():
	# look inside the virtualenv directory for the pip executable to see if it already exists
	# if not we will create a new virtualenv in the directory
	if not exists('virtualenv/bin/pip'):
		run(f'python3.6 -m venv virtualenv')

	# use the pip install command to update the server tools 
	# based on what's in the project's requirements.txt file
	run('./virtualenv/bin/pip3 install -r ./requirements.txt') 

def _create_or_update_dotenv():
	# the append command conditionally adds a line to a file if that line isn't already there
	append('.env', 'DJANGO_DEBUG_FALSE=y')
	append('.env', f'SITENAME={env.host}')

	current_contents = run('cat .env')  # set a variable to grab all contents of the .env file
	# if a secret key doesnt exist in the .env file (current_contents)
	# then create a new random key and set it in the file
	if 'DJANGO_SECRET_KEY' not in current_contents:
		new_secret = ''.join(random.SystemRandom().choices(
			'abcdefghijklmnopqrstuvwxyz0123456789', k=50
		))
		append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
	# use virtualenv version of python to make sure we get the venv version of django
	# to run the collectstatic command
	run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
	run('./virtualenv/bin/python manage.py migrate --noinput')




