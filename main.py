"""
Main entry point for the UAV Deconfliction System.
"""
import sys
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main function."""
    logger.info("UAV Deconfliction System initialized")
    print("System ready. Run tests or examples to verify setup.")

if __name__ == "__main__":
    main()