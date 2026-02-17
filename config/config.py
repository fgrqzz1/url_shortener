import os
from dotenv import load_dotenv
from configparser import ConfigParser
from pathlib import Path

_CONFIG_ENV_VAR = 'urlsh.cfg'
_DEFAULT_CONFIG_PATH = 'config/urlsh.cfg'

class Configuration:
    def __init__(self):
        self.config = None
        self.config_path = os.getenv(_CONFIG_ENV_VAR, _DEFAULT_CONFIG_PATH)
        self._read_cfg()
        self._load_settings()

    def _read_cfg(self):
        self.cfg = ConfigParser()
        if not Path(self.config_path).exists():
            raise FileNotFoundError(
                f"Конфигурационный файл не найден: {self.config_path}"
            )
        self.cfg.read(self.config_path)


    def _load_settings(self):
        app_section = self.cfg['app']
        self.app_name = os.getenv('APP_NAME', app_section.get('name', "URL Shortener"))
        self.version = os.getenv('VERSION', app_section.get('version', '1.0.0'))
        debug_env = os.getenv('DEBUG')
        if debug_env is not None:
            self.debug = debug_env.lower() in ('true', '1', 'yes')
        else:
            self.debug = app_section.getboolean('debug', fallback=False)
        
        db_section = self.cfg['database']
        db_host = os.getenv('DB_HOST', db_section.get('host', 'localhost'))
        db_port = os.getenv('DB_PORT', db_section.get('port', '5432'))
        db_user = os.getenv('DB_USER', db_section.get('user', 'postgres'))
        db_password = os.getenv('DB_PASSWORD', db_section.get('password', ''))
        db_name = os.getenv('DB_NAME', db_section.get('db_name', 'url_shortener'))
        db_engine = os.getenv('DB_ENGINE', db_section.get('engine', 'sqlite3'))

        sqlite_path = os.getenv('SQLITE_PATH', db_section.get('sqlite_path', './url_shortener.db'))
        self.database_url = f'sqlite:///{sqlite_path}'
        self.database_engine = db_engine

        server_section = self.cfg['server']
        self.host = os.getenv('HOST', server_section.get('host', '0.0.0.0'))
        self.port = int(os.getenv('PORT', server_section.get('port', '8000')))

        # todo: в переменную окружения
        self.secret_key = os.getenv('SECRET_KEY', self.cfg['app'].get('secret_key', 'dev-secret-key'))

        url_section = self.cfg.get('url', {})
        self.default_short_code_length = int(
            os.getenv('SHORT_CODE_LENGTH', url_section.get('default_length', '6'))
        )
    def __getattr__(self, name):
        if self.cfg is None:
            self._read_cfg()
        try: 
            return dict(self.cfg[name].items())
        except KeyError:
            raise AttributeError(f'Секция {name} не найдена в конфиге')


config = Configuration()