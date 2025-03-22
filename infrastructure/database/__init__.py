from infrastructure.database.models import init_db
database_url = 'sqlite:///chatbot.db'
init_db(database_url)