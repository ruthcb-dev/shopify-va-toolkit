import json
from copy import deepcopy
from pathlib import Path


class ConfigManager:
    """
    Loads, validates, and saves application settings.

    The config.json file is created automatically when it does not exist.
    """

    DEFAULT_SETTINGS = {
        "store_url": "",
        "output_folder": "output",
        "image_folder": "images",
        "csv_encoding": "utf-8-sig",
        "open_output_after_export": False,
        "confirm_exit": True
    }

    def __init__(self, config_file=None):

        project_root = Path(__file__).resolve().parent.parent

        if config_file:

            self.config_file = Path(config_file)

        else:

            self.config_file = (
                project_root
            / "app_config"
            / "config.json"
            )

        self.config_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================================
    # Default Settings
    # ==========================================================

    def get_default_settings(self):

        return deepcopy(
            self.DEFAULT_SETTINGS
        )

    # ==========================================================
    # Load Settings
    # ==========================================================

    def load_settings(self):

        if not self.config_file.exists():

            settings = self.get_default_settings()

            self.save_settings(settings)

            return settings

        try:

            with self.config_file.open(
                "r",
                encoding="utf-8"
            ) as file:

                loaded_settings = json.load(file)

            if not isinstance(
                loaded_settings,
                dict
            ):

                raise ValueError(
                    "Configuration data must be a JSON object."
                )

            settings = self.get_default_settings()

            settings.update(
                loaded_settings
            )

            settings = self.validate_settings(
                settings
            )

            return settings

        except (
            json.JSONDecodeError,
            OSError,
            ValueError,
            TypeError
        ):

            settings = self.get_default_settings()

            self.save_settings(settings)

            return settings

    # ==========================================================
    # Save Settings
    # ==========================================================

    def save_settings(self, settings):

        validated_settings = self.validate_settings(
            settings
        )

        temporary_file = self.config_file.with_suffix(
            ".tmp"
        )

        with temporary_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                validated_settings,
                file,
                indent=4,
                ensure_ascii=False
            )

        temporary_file.replace(
            self.config_file
        )

        return validated_settings

    # ==========================================================
    # Update Settings
    # ==========================================================

    def update_settings(self, updated_settings):

        current_settings = self.load_settings()

        current_settings.update(
            updated_settings
        )

        return self.save_settings(
            current_settings
        )

    # ==========================================================
    # Reset Settings
    # ==========================================================

    def reset_settings(self):

        default_settings = self.get_default_settings()

        return self.save_settings(
            default_settings
        )

    # ==========================================================
    # Validation
    # ==========================================================

    def validate_settings(self, settings):

        validated = self.get_default_settings()

        if not isinstance(settings, dict):

            return validated

        store_url = settings.get(
            "store_url",
            ""
        )

        if isinstance(store_url, str):

            validated["store_url"] = (
                store_url.strip()
            )

        output_folder = settings.get(
            "output_folder",
            "output"
        )

        if (
            isinstance(output_folder, str)
            and output_folder.strip()
        ):

            validated["output_folder"] = (
                output_folder.strip()
            )

        image_folder = settings.get(
            "image_folder",
            "images"
        )

        if (
            isinstance(image_folder, str)
            and image_folder.strip()
        ):

            validated["image_folder"] = (
                image_folder.strip()
            )

        csv_encoding = settings.get(
            "csv_encoding",
            "utf-8-sig"
        )

        allowed_encodings = {
            "utf-8-sig",
            "utf-8",
            "cp1252"
        }

        if csv_encoding in allowed_encodings:

            validated["csv_encoding"] = (
                csv_encoding
            )

        validated["open_output_after_export"] = bool(
            settings.get(
                "open_output_after_export",
                False
            )
        )

        validated["confirm_exit"] = bool(
            settings.get(
                "confirm_exit",
                True
            )
        )

        return validated