# coding: utf-8
"""Stakkr main controller. Used by the CLI to do all its actions."""

import os
from platform import system as os_name
import subprocess
import sys
import click
from clint.textui import colored, puts, columns
from stakkr import command, docker_actions as docker, package_utils
from stakkr.configreader import Config
from stakkr.proxy import Proxy


class StakkrActions():
    """Main class that does actions asked in the cli."""

    _services_to_display = {
        'adminer': {'name': 'Adminer', 'url': 'http://{}'},
        'apache': {'name': 'Web Server', 'url': 'http://{}'},
        'elasticsearch': {'name': 'ElasticSearch', 'url': 'http://{}'},
        'kibana': {'name': 'Kibana', 'url': 'http://{}'},
        'logstash': {'name': 'Logstash', 'url': 'http://{}'},
        'mailcatcher': {'name': 'Mailcatcher (fake SMTP)', 'url': 'http://{}', 'extra_port': 25},
        'maildev': {'name': 'Maildev (Fake SMTP)', 'url': 'http://{}', 'extra_port': 25},
        'nginx': {'name': 'Web Server', 'url': 'http://{}'},
        'phpmyadmin': {'name': 'PhpMyAdmin', 'url': 'http://{}'},
        'portainer': {'name': 'Portainer (Docker GUI)', 'url': 'http://{}'},
        'xhgui': {'name': 'XHGui (PHP Profiling)', 'url': 'http://{}'}
    }

    def __init__(self, base_dir: str, ctx: dict):
        """Set all require properties."""
        # Work with directories and move to the right place
        self.stakkr_base_dir = base_dir
        self.context = ctx
        self.cwd_abs = os.getcwd()
        self.cwd_relative = self._get_relative_dir()
        os.chdir(self.stakkr_base_dir)

        # Set some general variables
        self.config_file = ctx['CONFIG']
        self.compose_base_cmd = self._get_compose_base_cmd()
        self.cts = []
        self.running_cts = []

        # Get info from config
        self.config = self._get_config()
        self.main_config = self.config['main']
        self.project_name = self.main_config.get('project_name')

    def console(self, container: str, user: str, tty: bool):
        """Enter a container. Stakkr will try to guess the right shell."""
        docker.check_cts_are_running(self.project_name)

        tty = 't' if tty is True else ''
        ct_name = docker.get_ct_name(container)
        cmd = ['docker', 'exec', '-u', user, '-i' + tty]
        cmd += [docker.get_ct_name(container), docker.guess_shell(ct_name)]
        subprocess.call(cmd)

        command.verbose(self.context['VERBOSE'], 'Command : "' + ' '.join(cmd) + '"')

    def get_services_urls(self):
        """Once started, displays a message with a list of running containers."""
        cts = docker.get_running_containers(self.project_name)[1]

        text = ''
        for ct_id, ct_info in cts.items():
            if ct_info['compose_name'] not in self._services_to_display:
                continue

            options = self._services_to_display[ct_info['compose_name']]
            url = self.get_url(ct_info['ports'], options['url'], ct_info['compose_name'])
            name = colored.yellow(options['name'])
            text += '  - For {}'.format(name).ljust(55, ' ') + ' : ' + url + '\n'

            if 'extra_port' in options:
                port = str(options['extra_port'])
                text += ' '*4 + '(In your containers use the host '
                text += '"{}" and port {})\n'.format(ct_info['compose_name'], port)

        return text

    def exec_cmd(self, container: str, user: str, args: tuple, tty: bool):
        """Run a command from outside to any container. Wrapped into /bin/sh."""
        docker.check_cts_are_running(self.project_name)

        # Protect args to avoid strange behavior in exec
        args = ['"{}"'.format(arg) for arg in args]

        tty = 't' if tty is True else ''
        ct_name = docker.get_ct_name(container)
        cmd = ['docker', 'exec', '-u', user, '-i' + tty, ct_name, 'sh', '-c']
        cmd += ["""test -d "/var/{0}" && cd "/var/{0}" ; exec {1}""".format(self.cwd_relative, ' '.join(args))]
        command.verbose(self.context['VERBOSE'], 'Command : "' + ' '.join(cmd) + '"')
        subprocess.call(cmd, stdin=sys.stdin)

    def start(self, container: str, pull: bool, recreate: bool, proxy: bool):
        """If not started, start the containers defined in config."""
        verb = self.context['VERBOSE']
        debug = self.context['DEBUG']

        self._is_containers_running(container)

        if pull is True:
            command.launch_cmd_displays_output(self.compose_base_cmd + ['pull'], verb, debug, True)

        recreate_param = '--force-recreate' if recreate is True else '--no-recreate'
        cmd = self.compose_base_cmd + ['up', '-d', recreate_param, '--remove-orphans']
        cmd += self._get_single_container_option(container)

        command.verbose(self.context['VERBOSE'], 'Command: ' + ' '.join(cmd))
        command.launch_cmd_displays_output(cmd, verb, debug, True)

        self.running_cts, self.cts = docker.get_running_containers(self.project_name)
        if self.running_cts is 0:
            raise SystemError("Couldn't start the containers, run the start with '-v' and '-d'")

        self._run_iptables_rules()
        self._run_services_post_scripts()
        if proxy is True:
            network_name = docker.get_network_name(self.project_name)
            Proxy(self.config['proxy'].get('port')).start(network_name)

    def status(self):
        """Return a nice table with the list of started containers."""
        try:
            docker.check_cts_are_running(self.project_name)
        except SystemError:
            puts(colored.yellow('[INFO]') + ' stakkr is currently stopped')
            sys.exit(0)

        self._print_status_headers()
        self._print_status_body()

    def stop(self, container: str, proxy: bool):
        """If started, stop the containers defined in config. Else throw an error."""
        verb = self.context['VERBOSE']
        debug = self.context['DEBUG']

        docker.check_cts_are_running(self.project_name)

        cmd = self.compose_base_cmd + ['stop'] + self._get_single_container_option(container)
        command.launch_cmd_displays_output(cmd, verb, debug, True)

        self.running_cts, self.cts = docker.get_running_containers(self.project_name)
        if self.running_cts is not 0 and container is None:
            raise SystemError("Couldn't stop services ...")

        if proxy is True:
            network_name = docker.get_network_name(self.project_name)
            Proxy(self.config['proxy'].get('port')).stop()

    def _call_service_post_script(self, service: str):
        service_script = package_utils.get_file('static', 'services/{}.sh'.format(service))
        if os.path.isfile(service_script) is True:
            cmd = ['bash', service_script, docker.get_ct_item(service, 'name')]
            subprocess.call(cmd)
            command.verbose(self.context['VERBOSE'], 'Service Script : ' + ' '.join(cmd))

    def _get_compose_base_cmd(self):
        if self.context['CONFIG'] is None:
            return ['stakkr-compose']

        return ['stakkr-compose', '-c', self.context['CONFIG']]

    def _get_config(self):
        config = Config(self.config_file)
        main_config = config.read()
        if main_config is False:
            config.display_errors()
            sys.exit(1)

        return main_config

    def _get_single_container_option(self, container: str):
        if container is None:
            return []

        return [container]

    def _get_relative_dir(self):
        if self.cwd_abs.startswith(self.stakkr_base_dir):
            return self.cwd_abs[len(self.stakkr_base_dir):].lstrip('/')

        return ''

    def _is_containers_running(self, container: str):

        try:
            docker.check_cts_are_running(self.project_name)
        except SystemError:
            return

        if container is None:
            puts(colored.yellow('[INFO]') + ' stakkr is already started ...')
            sys.exit(0)

        # If single container : check if that specific one is running
        ct_name = docker.get_ct_item(container, 'name')
        if docker.container_running(ct_name):
            puts(colored.yellow('[INFO]') + ' service {} is already started ...'.format(container))
            sys.exit(0)

    def _print_status_headers(self):
        puts(columns(
            [(colored.green('Container')), 16], [colored.green('IP'), 15],
            [(colored.green('Url')), 32], [(colored.green('Image')), 32],
            [(colored.green('Docker ID')), 15], [(colored.green('Docker Name')), 25]
            ))

        puts(columns(
            ['-'*16, 16], ['-'*15, 15],
            ['-'*32, 32], ['-'*32, 32],
            ['-'*15, 15], ['-'*25, 25]
            ))

    def _print_status_body(self):
        self.running_cts, self.cts = docker.get_running_containers(self.project_name)

        for container in sorted(self.cts.keys()):
            ct_data = self.cts[container]
            if ct_data['ip'] == '':
                continue

            puts(columns(
                [ct_data['compose_name'], 16], [ct_data['ip'], 15],
                [ct_data['traefik_host'], 32], [ct_data['image'], 32],
                [ct_data['id'][:12], 15], [ct_data['name'], 25]
                ))

    def _run_iptables_rules(self):
        """For some containers we need to add iptables rules added from the config."""
        block_config = self.config['network-block']
        for service, ports in block_config.items():
            error, msg = docker.block_ct_ports(service, ports, self.project_name)
            if error is True:
                click.secho(msg, fg='red')
                continue

            command.verbose(self.context['VERBOSE'], msg)

    def _run_services_post_scripts(self):
        """
        Run services post scripts.

        A service can have a .sh file that will be executed once it's started.
        Useful to override some actions of the classical /run.sh.
        """
        if os.name == 'nt':
            click.secho('Could not run service post scripts under Windows', fg='red')
            return

        for service in self.main_config.get('services'):
            self._call_service_post_script(service)

    def get_url(self, ports: list, service_url: str, service: str):
        """Build URL to be displayed."""
        proxy_conf = self.config['proxy']
        # By default our URL is the IP
        url = docker.get_ct_item(service, 'ip')
        # If proxy enabled, display nice urls
        if int(proxy_conf['enabled']) is 1:
            url = docker.get_ct_item(service, 'traefik_host')
            url += '' if int(proxy_conf['port']) is 80 else ':{}'.format(proxy_conf['port'])
        elif os_name() in ['Windows', 'Darwin']:
            puts(colored.yellow('[WARNING]') + ' Under Win and Mac, you need the proxy enabled')

        return service_url.format(url)
