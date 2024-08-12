from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship



class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    admin_projects = relationship("Projects", back_populates="project_owner", cascade='all, delete')
    blogs = relationship("Blog", back_populates="blog_owner", cascade='all, delete')
    contacts = relationship("Contact", back_populates="contact_owner", cascade='all, delete')


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    project_link = Column(String, nullable=False)
    project_owner = relationship("AdminUser", back_populates="admin_projects")
    admin_id = Column(Integer, ForeignKey('admin_users.id'))



class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    admin_id = Column(Integer, ForeignKey('admin_users.id'))
    blog_owner = relationship("AdminUser", back_populates="blogs")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    phone = Column(Integer)
    linkedIn_URL = Column(String)
    admin_id = Column(Integer, ForeignKey('admin_users.id'))
    contact_owner = relationship("AdminUser", back_populates="contacts")
    

