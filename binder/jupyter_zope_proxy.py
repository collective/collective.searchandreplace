from notebook.utils import url_path_join as ujoin
from jupyter_server_proxy.handlers import AddSlashHandler
from jupyter_server_proxy.handlers import LocalProxyHandler
from jupyter_server_proxy.handlers import ProxyHandler
from tornado import web


def load_jupyter_server_extension(nbapp):
    base_url = nbapp.web_app.settings["base_url"]
    zope_handlers = make_handlers(base_url)
    nbapp.web_app.add_handlers(".*", zope_handlers)


def make_handlers(base_url):
    """
    get tornado handlers for registered server_processes
    """
    handlers = []
    name = "zope"
    handlers.append(
        (
            ujoin(base_url, r"/zope/(.*)"),
            ZopeLocalProxyHandler,
            #        dict(zope_port='9080'),
        )
    )
    handlers.append((ujoin(base_url, name), AddSlashHandler))
    return handlers


class ZopeLocalProxyHandler(LocalProxyHandler):
    def __init__(self, *args, **kwargs):
        self.port = kwargs.pop("zope_port", "8080")
        super().__init__(*args, **kwargs)
        self.proxy_base = "zope"

    def _build_proxy_request(self, host, port, proxied_path, body):
        uri_prefix = self.request.uri[: self.request.uri.find("/zope") + len("/zope")]
        uri_parts = [f"_vh_{part}" for part in uri_prefix.split("/") if part]
        vh = "/".join(uri_parts)
        zope_proxied_path = (
            f"/VirtualHostBase/{self.request.protocol}/{self.request.host}"
            f"/VirtualHostRoot/{vh}/{proxied_path}"
        )
        return super()._build_proxy_request(host, port, zope_proxied_path, body)

    async def http_get(self, path):
        return await self.proxy(self.port, path)

    async def open(self, path):
        return await super().open(self.port, path)

    def post(self, path):
        return self.proxy(self.port, path)

    def put(self, path):
        return self.proxy(self.port, path)

    def delete(self, path):
        return self.proxy(self.port, path)

    def head(self, path):
        return self.proxy(self.port, path)

    def patch(self, path):
        return self.proxy(self.port, path)

    def options(self, path):
        return self.proxy(self.port, path)
