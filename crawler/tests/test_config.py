import pytest
import yaml
from pathlib import Path


def test_load_config():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    assert config is not None


def test_config_has_required_fields():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    assert 'crawler' in config
    assert 'search_engines' in config['crawler']
    assert 'storage' in config['crawler']


def test_search_engines_list():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    engines = config['crawler']['search_engines']
    assert len(engines) >= 3
    assert 'google' in engines
    assert 'baidu' in engines


def test_storage_dirs():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    storage = config['crawler']['storage']
    assert 'data_dir' in storage
    assert 'sites_dir' in storage
    assert 'news_dir' in storage
