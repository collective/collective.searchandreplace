import os
import sys
import time
import subprocess
import pathlib2 as pathlib
import socket
from contextlib import closing


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


class ZopeInstance(object):
    def __init__(
        self,
        tmp_path,
        pytestconfig,
        host="127.0.0.1",
        port=8080,
    ):
        self.host = host
        self.port = port
        buildout_exe = pathlib.Path(
            pytestconfig.invocation_dir, sys.argv[0]
        ).parent.joinpath("buildout")
        package_path = pytestconfig.rootdir
        buildout_cfg = pathlib.Path(tmp_path, "buildout.cfg")
        buildout = u"""
[buildout]
extends =  %(package_path)s/buildout.cfg
develop =  %(package_path)s
""" % dict(
            package_path=package_path
        )
        with buildout_cfg.open("w") as f:
            f.write(buildout)
        os.chdir(str(tmp_path))
        retcode = subprocess.call([str(buildout_exe), "bootstrap"])
        assert retcode == 0
        output = subprocess.check_output(
            [str(buildout_exe), "query", "buildout:eggs-directory"]
        )

        self.eggs_directory = output.decode("utf8").split("\n")[-2]

        output = subprocess.check_output(["bin/buildout", "query", "buildout:develop"])
        assert str(package_path).encode("utf8") in output

        output = subprocess.check_output(["bin/buildout", "query", "instance:recipe"])
        assert b"plone.recipe.zope2instance" in output

        output = subprocess.check_output(["bin/buildout", "query", "plonesite:recipe"])
        assert b"collective.recipe.plonesite" in output

    def run_buildouts(self, from_version):
        print()
        print("Plone site with", from_version)
        retcode = subprocess.call(
            [
                "bin/buildout",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "buildout:develop=",
                "versions:%s" % from_version,
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()
        print()
        print("Plone site with develop")
        retcode = subprocess.call(
            [
                "bin/buildout",
                "buildout:eggs-directory=%s" % self.eggs_directory,
                "install",
                "instance",
                "plonesite",
            ]
        )
        assert retcode == 0
        assert pathlib.Path("bin/instance").exists()

    def start(self):
        self.process = subprocess.Popen(["bin/instance", "console"])
        # retcode = subprocess.call(["bin/instance", "start"])
        # assert retcode == 0
        while not check_socket(self.host, self.port):
            time.sleep(0.3)

    def stop(self):
        self.process.terminate()
        # retcode = subprocess.call(["bin/instance", "stop"])
        # assert retcode == 0

    __enter__ = start

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
