bin/pip3:
	virtualenv -p 3 .

bin/buildout: bin/pip3
	bin/pip3 install -r requirements.txt

clean:
	rm -rf bin/ lib/ include/ parts/ .installed.cfg

plone52: bin/buildout
	bin/buildout -v buildout:extends="plone52.cfg versions.cfg"

plone60: bin/buildout
	bin/buildout -v buildout:extends="plone60.cfg versions.cfg"

test:
	bin/pytest
