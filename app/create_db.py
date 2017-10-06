import os, sys
from main import db
import dummy

if __name__ == '__main__':
    db.create_all()
    dummy.first_data()