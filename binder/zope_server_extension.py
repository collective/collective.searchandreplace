from subprocess import Popen
import os


def load_jupyter_server_extension(nbapp):
    """serve zope instance"""
    instance_cmd = os.path.join(nbapp.notebook_dir, "bin", "instance")
    Popen([instance_cmd, "console"])
