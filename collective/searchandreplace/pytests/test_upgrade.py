import sys
import os
import time
import pytest
import subprocess
import requests
import pathlib2 as pathlib
import socket
from contextlib import closing


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


@pytest.fixture
def plone_instance(tmp_path, pytestconfig):
    buildout_exe = pathlib.Path(
        pytestconfig.invocation_dir,
        sys.argv[0]
    ).parent.joinpath('buildout')
    return ZopeInstance(tmp_path, buildout_exe, pytestconfig.rootdir)


class ZopeInstance(object):

    def __init__(
            self,
            tmp_path,
            buildout_exe,
            package_path,
            host='127.0.0.1',
            port=8080,
            ):
        self.host = host
        self.port = port
        buildout_cfg = pathlib.Path(tmp_path, 'buildout.cfg')
        buildout = u"""
[buildout]
extends =  %(package_path)s/buildout.cfg
develop =  %(package_path)s
""" % dict(package_path=package_path)
        with buildout_cfg.open("w") as f:
            f.write(buildout)
        os.chdir(str(tmp_path))
        subprocess.call([str(buildout_exe), "bootstrap"])

        output = subprocess.check_output(
            ["bin/buildout", "query", "buildout:develop"]
        )
        assert str(package_path) in output

        output = subprocess.check_output(
            ["bin/buildout", "query", "instance:recipe"]
        )
        assert 'plone.recipe.zope2instance' in output

        output = subprocess.check_output(
            ["bin/buildout", "query", "plonesite:recipe"]
        )
        assert 'collective.recipe.plonesite' in output

    def run_buildouts(self, from_version):
        subprocess.call(
            [
                "bin/buildout",
                "buildout:develop=",
                "versions:%s" % from_version,
                "install",
                "instance",
                "plonesite"
            ]
        )
        assert pathlib.Path("bin/instance").exists()
        subprocess.call(["bin/buildout", "install", "instance", "plonesite"])
        assert pathlib.Path("bin/instance").exists()

    def start(self):
        subprocess.call(["bin/instance", "start"])
        while not check_socket(self.host, self.port):
            time.sleep(.3)

    def stop(self):
        subprocess.call(["bin/instance", "stop"])

    __enter__ = start
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def test(plone_instance):
    plone_instance.run_buildouts("collective.searchandreplace=8.0.0")
    with plone_instance:
        r = requests.get(
            "http://localhost:8080/Plone/@@searchreplace-controlpanel",
            auth=('admin', 'admin')
        )
        assert r.status_code == 200
