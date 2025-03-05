from database import db

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    is_open = db.Column(db.Boolean, default=True)
    opening_hours = db.Column(db.String(255), nullable=True)

    #  Relationship: Menu Items Available at this Branch
    menu_items = db.relationship("MenuItem", secondary="menu_item_branches", backref="branches")

    def __repr__(self):
        return f"<Branch {self.name} - Open: {self.is_open}>"