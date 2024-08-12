from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..database import get_db
from ..models import models
from ..authentication import token_gen

router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']

)

@router.post('/', response_model=schemas.ShowBlog, status_code=status.HTTP_200_OK)
def create_blog(request:schemas.Blog, db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)): 
    new_blog = models.Blog(title=request.title, content=request.content, admin_id=admin_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_blog(request:schemas.Blog, id, db: Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    blog_edit = db.query(models.Blog).filter(models.Blog.id == id)
    if blog_edit.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} does not exist")
    else:
        blog_edit.update({models.Blog.title:request.title, models.Blog.content:request.content}, synchronize_session=False)
        # save the changes
        db.commit()
   
    return {"message": "Blog Updated sucessful"}


@router.delete('/delete/{id}')
def delete_blog(id, db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first() is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with {id} does not exist")

    blog.delete()
    # save the changes
    db.commit()
    return {"message":f"Blog with {id} deleted successfully"}


@router.delete('/delete_all/')
def delete_all(db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    all_blog = db.query(models.Blog)
    if all_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Blogs")
    all_blog.delete()
    db.commit()
    return {"message": "All blogs deleted successfully"}
