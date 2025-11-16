from sqlalchemy import false

from . import db

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    WhatsappNumber = db.Column(db.String(64), nullable=False)
    Location = db.Column(db.String(64), nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=True)
    birthtime = db.Column(db.String(12), nullable=True)
    ProfileImage = db.Column(db.String(64) , nullable=True)
    NIC_Number = db.Column(db.String(64) , nullable=True)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'WhatsappNumber' : self.WhatsappNumber,
            'Location' : self.Location,
            'DateOfBirth' : self.DateOfBirth.isoformat() if self.DateOfBirth else None,
            'birthtime' : self.birthtime,
            'ProfileImage' : self.ProfileImage,
            'NIC_Number' : self.NIC_Number,
            'password' : self.password
        }



