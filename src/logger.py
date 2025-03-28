import logging
import os 
from datetime import datetime 
def setup_logger(name=__name__,log_level=logging.INFO,log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #console handler 
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    #file handler 
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger


log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

current_time = datetime.now()
log_file_name = f"app_{current_time.strftime('%Y%m%d_%H%M%S')}.log"
log_file_path = os.path.join(os.getcwd(), "logs", log_file_name)
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = setup_logger(log_level=log_level, log_file=log_file_path)

if __name__ == "__main__":
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")