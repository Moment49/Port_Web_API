from typing import Annotated, List
from pydantic import BaseModel

# Schemas
class AdminBase(BaseModel):
    fullname: str
    email: str
    password: str
class CreateAdmin(AdminBase):
    class Config:
        orm_mode = True

class ShowAdminBase(BaseModel):
    fullname: str
    class Config:
        orm_mode = True 
     

class ProjectBase(BaseModel):
    project_name:str
    project_link: str

class CreateProject(ProjectBase):
    class Config:
        orm_mode = True

   
class ShowProject(BaseModel):
    project_name:str
    project_link: str
    project_owner: ShowAdminBase
    
    class Config:
        orm_mode = True

class EditProject(ProjectBase):
    class Config:
        orm_mode = True


class AdminLogin(BaseModel):
    username: str
    password: str


class BlogBase(BaseModel):
    title: str
    content: str

class Blog(BlogBase):
    class Config:
        orm_mode = True

class ShowBlog(Blog):
    blog_owner: ShowAdminBase


class ContactBase(BaseModel):
    email: str
    phone: int
    linkedIn_URL: str

class Contact(ContactBase):
    class Config:
        orm_mode = True

class ShowContact(Contact):
    contact_owner:ShowAdminBase


class ShowAdmin(BaseModel):
    fullname: str
    email: str
    admin_projects: List[ShowProject] = []
    blogs : List[ShowBlog] = []
    contacts: List[ShowContact] = []
    # contacts = List[ShowContact] = []
    class Config:
        orm_mode = True