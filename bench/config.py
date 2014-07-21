import os
import getpass
import json
from jinja2 import Environment, PackageLoader
from .utils import get_sites, get_config

env = Environment(loader=PackageLoader('bench', 'templates'), trim_blocks=True)

def generate_supervisor_config(bench='.'):
	template = env.get_template('supervisor.conf')
	bench_dir = os.path.abspath(bench)
	sites_dir = os.path.join(bench_dir, "sites")
	sites = get_sites(bench=bench)
	user = getpass.getuser()
	with open("sites/currentsite.txt") as f:
		default_site = f.read().strip()

	config = template.render(**{
		"bench_dir": bench_dir,
		"sites_dir": sites_dir,
		"user": user,
	})
	with open("config/supervisor.conf", 'w') as f:
		f.write(config)

def get_site_config(site, bench='.'):
	with open(os.path.join(bench, 'sites', site, 'site_config.json')) as f:
		return json.load(f)

def get_sites_with_config(bench='.'):
	sites = get_sites()
	return [{
		"name": site, 
		"port": get_site_config(site, bench=bench).get('nginx_port')
	} for site in sites]

def generate_nginx_config(bench='.'):
	template = env.get_template('nginx.conf')
	bench_dir = os.path.abspath(bench)
	sites_dir = os.path.join(bench_dir, "sites")
	sites = get_sites_with_config(bench=bench)
	user = getpass.getuser()
	with open("sites/currentsite.txt") as f:
		default_site = f.read().strip()
	default_site = {
		'name': default_site
	}

	config = template.render(**{
		"sites_dir": sites_dir,
		"default_site": default_site,
		"dns_multitenant": get_config().get('dns_multitenant'),
		"sites": sites
	})
	with open("config/nginx.conf", 'w') as f:
		f.write(config)