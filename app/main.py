from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal, get_db
from .authentication import auth
from .models import models
from .routes import projects, blogs, contacts


app = FastAPI(
    prefix= '/',
    tags=['Landing Page']
)

# create the database
models.Base.metadata.create_all(bind=engine)



@app.get('/', tags=['Landing Page'])
def index():
    return {"Message": "Welcome to My Portfolio Webiste"}

@app.get('/blogs',  tags=['Landing Page'])
def show_blog(db: Session = Depends(get_db)):

    all_blogs = db.query(models.Blog)
    if not all_blogs.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Blogs") 
    return  all_blogs

@app.get('/projects', tags=['Landing Page'])
def show_projects(db: Session = Depends(get_db)):
    all_projects = db.query(models.Projects)
    if not all_projects.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Projects")
    
    return  all_projects

@app.get('/contacts', tags=['Landing Page'])
def show_contacts(db: Session = Depends(get_db)):
    all_contacts = db.query(models.Contact)
    if not all_contacts.all():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Contacts")
    
    return  all_contacts


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(blogs.router)
app.include_router(contacts.router)
