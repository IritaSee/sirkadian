from db import db

class TagsModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column('id', db.Integer, primary_key=True)
    tag = db.Column('tag', db.String(80), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'tag': self.tag,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter_by(tag=tag).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()