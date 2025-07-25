from src.utils.manage_config import ConfigManager

# Create a ConfigManager instance
config_manager = ConfigManager("../config/basic_config.yaml")

# Step 1: Load and print the original configuration
print("Original Configuration:")
print(config_manager.get_config())

# Step 2: Insert or Update a configuration key
config_manager.insert("sector.sector_board_info", "remote_host")  # Update existing key
config_manager.insert("sector.hist_price_em", "127.0.0.1")  # Add new key

print("\nAfter Insert/Update:")
print(config_manager.get_config())

# Step 3: Delete a key from the configuration
config_manager.delete("etf.max_retries")  # Delete a list (handlers) under logging

print("\nAfter Deletion:")
print(config_manager.get_config())

# Step 4: List all configuration keys
print("\nListing All Configuration Keys:")
config_manager.list_keys()
