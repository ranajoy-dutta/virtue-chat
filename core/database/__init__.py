from core.database.models import init_db
from config.config_loader import ConfigLoader

config = ConfigLoader()
database_url = config.database.url
init_db(database_url)