import pytest
import requests
import pathlib2 as pathlib
from zope_instance import ZopeInstance


@pytest.fixture
def plone_instance(tmp_path, pytestconfig):
    return ZopeInstance(tmp_path, pytestconfig)


def test(plone_instance):
    plone_instance.run_buildouts("collective.searchandreplace=8.0.0")
    with plone_instance:
        r = requests.get(
            "http://localhost:8080/Plone/@@searchreplace-controlpanel",
            auth=('admin', 'admin')
        )
        assert r.status_code == 200
