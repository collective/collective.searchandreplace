bin/pip3:
	virtualenv -p 3 .

bin/buildout: bin/pip3
	bin/pip3 install -r requirements-plone60.txt

clean:
	rm -rf bin/ lib/ include/ parts/ .installed.cfg

plone52: bin/buildout
	bin/buildout -v buildout:extends="test-5.2.x.cfg versions.cfg"

plone60: bin/buildout
	bin/buildout -v buildout:extends="test-6.0.x.cfg versions.cfg"

test:
	bin/pytest
