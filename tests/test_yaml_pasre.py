from src import yaml_parse


def test_get_build_set():
    data = yaml_parse.get_build_set()
    assert data == {'builds': []}
