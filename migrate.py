import os

os.environ['MIGRATION'] = '1'

if not os.getenv('FLASK_ENV') == 'production':
    print("Loading environment variables from .env")
    from dotenv import load_dotenv
    load_dotenv()


import peeweedbevolve
from models import db

print("Running Migration")
if os.getenv('FLASK_ENV') == 'production':
    db.evolve(ignore_tables={'base_model'}, interactive=False)
else:
    db.evolve(ignore_tables={'base_model'})
print("Finish Migration")

# if __name__ == '__main__':
#    db.evolve(ignore_tables={'base_model'})