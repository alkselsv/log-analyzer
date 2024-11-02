"""Определение класса Scanner"""
import os
import json
from logging import Logger


class LogScanner:
    """Сканер логов"""

    def __init__(self, root_dir: str = "users", logger: Logger | None = None) -> None:
        self.root_dir: str = root_dir
        self.logger: Logger | None = logger
        self.models: list[str | None] = []
        self.min_bounds: list[float] = []
        self.log_files: list[str] = []

    def scan(self) -> None:
        """Выполняет поиск файлов settings.json и загружет из них настройки"""
        for user_id in ["1"]:
            user_dir = os.path.join(self.root_dir, user_id)
            if os.path.isdir(user_dir):
                for site_id in ["200_kitzap.ru"]:
                    site_dir = os.path.join(user_dir, site_id)
                    if os.path.isdir(site_dir):
                        settings_file = os.path.join(site_dir, "settings.json")
                        if os.path.isfile(settings_file):
                            with open(settings_file, "r", encoding="utf8") as file:
                                settings = json.load(file)
                                self.models.append(settings.get("model"))
                                self.min_bounds.append(
                                    settings.get("min_bound_per") / 100
                                )
                        log_file = os.path.join(site_dir, "logs", "sp.json.log")
                        if os.path.isfile(log_file):
                            self.log_files.append(log_file)
        self.logger.info(f"Found log files: {self.log_files}")
        self.logger.info(f"Found model files: {self.models}")

    def get_models(self) -> list[str | None]:
        """Возвращает список моделей"""
        return self.models

    def get_min_bounds(self) -> list[float]:
        """Возвращает пороговых значений"""
        return self.min_bounds

    def get_log_files(self) -> list[str]:
        """Возвращает список путей к файлам"""
        return self.log_files
