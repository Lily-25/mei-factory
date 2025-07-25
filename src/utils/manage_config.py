import yaml
import os


class ConfigManager:
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.config = self.load()

    def load(self):
        """Load the YAML configuration file into a Python dictionary."""
        if not os.path.exists(self.config_file):
            print(f"Notice: {self.config_file} does not exist. System will create a empty file")
            data = {}
            with open(self.config_file, "w") as file:
                yaml.dump(data, file)
            return {}
        with open(self.config_file, "r") as f:
            return yaml.safe_load(f) or {}

    def _save(self):
        """Save the current configuration back to the YAML file."""
        with open(self.config_file, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def insert(self, key, value):
        """Insert or update a specific key-value pair in the configuration."""
        keys = key.split(".")  # Allow nested keys using dot notation (e.g., "database.host")
        temp_config = self.config

        # Traverse the config structure to the right level
        for part in keys[:-1]:
            temp_config = temp_config.setdefault(part, {})

        # Insert or update the final key
        temp_config[keys[-1]] = value
        self._save()

    def update(self, key, value):
        """Update an existing key in the configuration."""
        self.insert(key, value)  # Insertion automatically handles update as well

    def delete(self, key):
        """Delete a specific key from the configuration."""
        keys = key.split(".")
        temp_config = self.config

        # Traverse to the right level
        for part in keys[:-1]:
            temp_config = temp_config.get(part, {})

        # Delete the final key
        if keys[-1] in temp_config:
            del temp_config[keys[-1]]
            print(f"Deleted {key} from configuration.")
            self._save()
        else:
            print(f"Error: {key} not found.")

    def list_keys(self):
        """List all keys in the configuration, including nested keys."""
        self._print_keys(self.config, "")

    def _print_keys(self, config, parent_key):
        """Recursive function to print keys and their nested structure."""
        if isinstance(config, dict):
            for key, value in config.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                self._print_keys(value, full_key)
        else:
            print(f"{parent_key}: {config}")

    def get_config(self):
        """Get the current configuration as a dictionary."""
        return self.config
