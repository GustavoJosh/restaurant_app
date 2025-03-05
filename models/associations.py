# models/associations.py
from database import db

menu_item_branches = db.Table(
    'menu_item_branches',
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_items.id', ondelete="CASCADE"), primary_key=True),
    db.Column('branch_id', db.Integer, db.ForeignKey('branches.id', ondelete="CASCADE"), primary_key=True)
)