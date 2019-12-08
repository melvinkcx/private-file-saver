import json

from core.configs import ConfigManager


def test_creates_default_config_file(tmpdir):
    config_file_path = tmpdir.join("config.json")
    config_manager = ConfigManager(config_file_path=config_file_path)
    with open(config_file_path) as f:
        config_read = json.loads(f.read())

    assert config_read == config_manager.default_config, "Config files is not properly created"


def test_config_file_is_correctly_loaded(tmpdir):
    config = {
        # Transfer Config
        'READ_CHUNK_SIZE': 8 * 1024,  # 8KB
        'MULTIPART_THRESHOLD': 1 * 1024 ** 2,  # 1MB
        'MULTIPART_CHUNKSIZE': 8 * 1024 ** 2,  # 1MB
        'MAX_CONCURRENCY': 4,
        'AWS_ACCESS_KEY_ID': "aws_access_key_id",
        'AWS_SECRET_ACCESS_KEY': "aws_secret_access_key",
        'AWS_REGION': "aws_region",
        'DEFAULT_BUCKET_NAME': "aws_default_bucket_name",
        'TARGET_PATH': str(tmpdir)
    }
    config_file_path = tmpdir.join("config.json")
    config_file_path.write(json.dumps(config))

    config_manager = ConfigManager(config_file_path=config_file_path)
    assert config_manager.config == config, "Config file is not correctly loaded"


def test_list_configurables(tmpdir):
    config_file_path = tmpdir.join("config.json")
    config_manager = ConfigManager(config_file_path=config_file_path)
    configurables = config_manager.list_configurables()
    assert set(configurables).issubset({
        'READ_CHUNK_SIZE', 'MULTIPART_THRESHOLD', 'MULTIPART_CHUNKSIZE', 'MAX_CONCURRENCY', 'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'DEFAULT_BUCKET_NAME', 'TARGET_PATH'})


def test_set_config(tmpdir):
    config_file_path = tmpdir.join("config.json")
    config_manager = ConfigManager(config_file_path=config_file_path)
    config_manager.set("READ_CHUNK_SIZE", 1000)
    assert config_manager.get("READ_CHUNK_SIZE") == 1000
    config_saved = json.loads(config_file_path.read())
    assert config_saved.get("READ_CHUNK_SIZE") == 1000


def test_set_many(tmpdir):
    config_file_path = tmpdir.join("config.json")
    config_manager = ConfigManager(config_file_path=config_file_path)
    config_manager.set_many({
        "READ_CHUNK_SIZE": 1000,
        "AWS_SECRET_ACCESS_KEY": "123454321"
    })
    assert config_manager.get("READ_CHUNK_SIZE") == 1000
    assert config_manager.get("AWS_SECRET_ACCESS_KEY") == "123454321"
    config_saved = json.loads(config_file_path.read())
    assert config_saved.get("READ_CHUNK_SIZE") == 1000
    assert config_saved.get("AWS_SECRET_ACCESS_KEY") == "123454321"
