import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)
from models import page_model
from repositories import page_repository

import sqlite3

session = sqlite3.connect('../page.db')

emptypage = page_model.Page(pageid=1).page

class TestRepositoryLayer:


   @staticmethod
    def test_repo_get_all():
        repo = page_repository.SQLiteRepository(session)
        pages = repo.get_all()
        cursor = session.cursor()
        expected = cursor.execute(""" SELECT * FROM pages """).fetchall()
        assert expected == pages

    @staticmethod
    def test_repo_can_add_page():
        # TO DO: Note that the repository should interact with the DB and with the Domain model. 
        # This means the repo should get the page model structure from the page_model.
        p = {'id': 829, 'title': 'SQLite', 'header': 'with python', 'author': 'Gianni', 'body': 'OK'}
        #page = page_model.Page(p)
        repo = page_repository.SQLiteRepository(session)
        repo.insert(p)
        id = p['id']
        cursor = session.cursor()
        expected = cursor.execute(""" SELECT * FROM pages WHERE id=? """, (id, )).fetchone()
        session.commit()
        assert  expected[1] == p['title']
    
    @staticmethod
    def test_repo_get_a_page():
        # here the get_from_id repository method is tested.
        id = 829
        repo = page_repository.SQLiteRepository(session)
        page = repo.get_by_id(id)
        session.close()
        assert page[1] == 'SQLite'


