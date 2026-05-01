from platformdirs import PlatformDirs
from pathlib import Path
import tempfile
import json
import os


class DirectoryManager():
    """Configuration and data Manager."""

    def __init__(self):
        """Initialice."""
        if os.geteuid() == 0:
            # Use /usr/local/share instead of /root when running as root
            self.dirs = PlatformDirs("CharGal", appauthor=False,
                                     use_site_for_root=True)
        else:
            self.dirs = PlatformDirs("CharGal", appauthor=False)

    def getConfigPath(self):
        """Get the config dir from the system."""
        return self.dirs.user_config_path

    def getDataDir(self):
        """Get tge data dir from the system."""
        return self.dirs.user_data_dir

    def saveConfig(self, config):
        """Save the configuration file."""
        dir = self.getConfigPath()
        file = dir / "config.json"

        configData = json.dumps(config, indent=4)

        try:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(configData)
            print("written config on " + file.as_uri())
        except (OSError, PermissionError) as e:
            tempDir = Path(tempfile.gettempdir()) / "CharGal"
            tempDir.mkdir(parents=True, exist_ok=True)
            file = tempDir / "config.json"
            file.write_text(configData)
            # TODO: Show error message in a dialog
            print(e)

    def loadConfig(self):
        """Load configuration file."""
        config = {}

        for configDir in self.dirs.iter_config_paths():
            file = configDir / "config.json"
            if file.exists():
                config.update(json.loads(file.read_text()))

        return config
