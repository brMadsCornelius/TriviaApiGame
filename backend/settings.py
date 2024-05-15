from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USERNAME=os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_TEST_NAME = os.environ.get("DATABASE_TEST_NAME")