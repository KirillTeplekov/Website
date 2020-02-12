from main import db


# Slide table
class Slide(db.Model):
    __tablename__ = 'slides'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    source = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    visible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Slide {} {} {} {} {}>'.format(
            self.id, self.name, self.source, self.description, self.visible)


# Images table
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return '<Image {} {}>'.format(
            self.id, self.source)


# Correspondents table
class Correspondent(db.Model):
    __tablename__ = 'correspondents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    photo = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<Correspondent {} {} {} {}>'.format(
            self.id, self.name, self.surname, self.description)


# Admins table
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))
    action = db.relationship("Action", backref='admins')

    def __repr__(self):
        return '<Admin {} {} {}>'.format(
            self.id, self.name, self.surname)


# Invites table
class Invite(db.Model):
    __tablename__ = 'invites'
    id = db.Column(db.Integer, primary_key=True)
    invite_text = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Correspondent {} {}>'.format(
            self.id, self.invite_text)


# Issues tables
class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return '<Issues {} {}>'.format(
            self.id, self.filename)


# Table with admin's actions
class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Issues {} {}>'.format(
            self.id, self.filename)


# News table
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(80), unique=False, nullable=False)
    text_path = db.Column(db.String(200), unique=True, nullable=False)
    image_path = db.Column(db.String(200), unique=True, nullable=True)

    def __repr__(self):
        return '<News {} {} {}>'.format(
            self.id, self.heading, self.text_path)
