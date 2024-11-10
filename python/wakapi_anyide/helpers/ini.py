import configparser
from pathlib import Path
from typing import Any, Dict
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from pydantic_settings.sources import ConfigFileSourceMixin, InitSettingsSource

class IniConfigSettingsSource(InitSettingsSource, ConfigFileSourceMixin):
    _config_dict: Dict[str, Any]
    
    def __init__(self, settings_cls: type[BaseSettings]):
        file = settings_cls.model_config.get("ini_file")
        assert file
        
        super().__init__(settings_cls, self._read_files(file))
    
    def _read_file(self, path: Path) -> dict[str, Any]:
        parsed = configparser.ConfigParser()
        parsed.read(path)
        return {section: dict(parsed[section]) for section in parsed.sections()}