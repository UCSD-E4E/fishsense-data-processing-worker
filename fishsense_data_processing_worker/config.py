'''Config
'''
import logging
import logging.handlers
import os
import time
from pathlib import Path
from typing import Dict

import platformdirs
from dynaconf import Dynaconf, Validator

IS_DOCKER = os.environ.get('E4EFS_DOCKER', False)
platform_dirs = platformdirs.PlatformDirs('e4efs_worker')


def get_log_path() -> Path:
    """Get log path

    Returns:
        Path: Path to log directory
    """
    if IS_DOCKER:
        return Path('/e4efs/logs')
    log_path = platform_dirs.user_log_path
    log_path.mkdir(parents=True, exist_ok=True)
    return log_path


def get_data_path() -> Path:
    """Get data path

    Returns:
        Path: Path to data directory
    """
    if IS_DOCKER:
        return Path('/e4efs/data')
    data_path = platform_dirs.user_data_path
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path


def get_config_path() -> Path:
    """Get config path

    Returns:
        Path: Path to config directory
    """
    if IS_DOCKER:
        return Path('/e4efs/config')
    config_path = Path('.')
    return config_path


def get_cache_path() -> Path:
    """Get cache path

    Returns:
        Path: Path to cache directory
    """
    if IS_DOCKER:
        return Path('/e4efs/cache')
    cache_path = platform_dirs.user_cache_path
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


validators = [
    Validator(
        'core.orchestrator',
        cast=str,
        required=True
    ),
    Validator(
        'core.api_key',
        required=True,
        cast=str
    ),
    Validator(
        'core.worker_name',
        required=True,
        cast=str
    ),
    Validator(
        'core.max_cpu',
        default=1,
        cast=int
    ),
    Validator(
        'core.max_gpu',
        default=1,
        cast=int
    ),
    Validator(
        'core.max_batch_size',
        default=50,
        cast=int
    )
]

settings = Dynaconf(
    envvar_prefix='E4EFS',
    environments=False,
    settings_files=[
        (get_config_path() / 'settings.toml').as_posix(),
        (get_config_path() / '.secrets.toml').as_posix()],
    merge_enabled=True,
    validators=validators
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.


def configure_logging():
    """Configures logging
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    log_dest = get_log_path().joinpath('e4efs_service.log')
    print(f'Logging to "{log_dest.as_posix()}"')

    log_file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_dest,
        when='midnight',
        backupCount=5
    )
    log_file_handler.setLevel(logging.DEBUG)

    msg_fmt = '%(asctime)s.%(msecs)03dZ - %(name)s - %(levelname)s - %(message)s'
    root_formatter = logging.Formatter(msg_fmt, datefmt='%Y-%m-%dT%H:%M:%S')
    log_file_handler.setFormatter(root_formatter)
    root_logger.addHandler(log_file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    error_formatter = logging.Formatter(msg_fmt, datefmt='%Y-%m-%dT%H:%M:%S')
    console_handler.setFormatter(error_formatter)
    root_logger.addHandler(console_handler)
    logging.Formatter.converter = time.gmtime

    logging_levels: Dict[str, str] = {
    }
    for logger_name, level in logging_levels.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.getLevelNamesMapping()[level])

    logging.info('Log path: %s', get_log_path())
    logging.info('Data path: %s', get_data_path())
    logging.info('Config path: %s', get_config_path())
