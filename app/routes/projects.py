from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..database import get_db
from ..models import models
from ..authentication import token_gen

router = APIRouter(
    prefix= '/project',
    tags=['Projects']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowProject)
def create_project(request:schemas.CreateProject, db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    new_project = models.Projects(project_name=request.project_name, project_link=request.project_link, admin_id=admin_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_project(request:schemas.EditProject, id, db: Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    project_edit = db.query(models.Projects).filter(models.Projects.id == id)
    if project_edit.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with {id} does not exist")
    else:
        project_edit.update({models.Projects.project_name:request.project_name, models.Projects.project_link:request.project_link}, synchronize_session=False)
        # save the changes
        db.commit()
   
    return {"message": "Project Updated sucessful"}


@router.delete('/delete/{id}')
def delete_project(id, db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    proj = db.query(models.Projects).filter(models.Projects.id == id)
    print(proj)
    if proj.first() is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with {id} does not exist")

    proj.delete()
    # save the changes
    db.commit()
    return {"message":f"Project with {id} deleted successfully"}


@router.delete('/delete_all/')
def delete_all(db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    all_projects = db.query(models.Projects)
    if all_projects is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Projects")
    all_projects.delete()
    db.commit()
    return {"message": "All projects deleted successfully"}

