#!/usr/bin/env python3
"""
Configuration manager for YouTube Downloader GUI
Handles saving and loading user preferences
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".youtube_downloader_gui"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "download_path": str(Path.home() / "Downloads"),
            "default_format": "best",
            "audio_only": False,
            "playlist_mode": False,
            "audio_format": "best",
            "window_geometry": "800x600",
            "last_url": ""
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                #Merge with defaults to handle new config options
                config = self.default_config.copy()
                config.update(loaded_config)
                return config
            else:
                return self.default_config.copy()
        except Exception:
            return self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass  #Fail silently if we can't save config
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
    
    def update(self, **kwargs):
        """Update multiple configuration values"""
        self.config.update(kwargs)
