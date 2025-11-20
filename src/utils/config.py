"""
Configuration management for the deconfliction system.
"""

class Config:
    """Base configuration."""
    
    # Spatial parameters
    SAFETY_BUFFER_DISTANCE = 50.0  # meters
    POSITION_TOLERANCE = 1.0  # meters
    
    # Temporal parameters
    TIME_STEP = 1.0  # seconds for interpolation
    TEMPORAL_TOLERANCE = 0.5  # seconds

    # Stage 5 sampling
    NUM_SAMPLES = 50

    # Visualization
    PLOT_DPI = 100
    ANIMATION_FPS = 10
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/deconfliction.log"
    
    # Testing
    TEST_DATA_PATH = "data/"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    SAFETY_BUFFER_DISTANCE = 100.0  # Stricter in production


def get_config(environment: str = "development") -> Config:
    """Get configuration based on environment."""
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
    }
    return configs.get(environment, DevelopmentConfig)()