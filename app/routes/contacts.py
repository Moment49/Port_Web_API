from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..database import get_db
from ..models import models
from ..authentication import token_gen

router = APIRouter(
    prefix='/contacts',
    tags=['Contacts']

)

@router.post('/', response_model=schemas.ShowContact, status_code=status.HTTP_200_OK)
def create_contact(request:schemas.Contact, db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)): 
    new_contact = models.Contact(email=request.email, phone=request.phone, linkedIn_URL=request.linkedIn_URL, admin_id=admin_id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.put('/edit/{id}', status_code=status.HTTP_200_OK)
def edit_contact(request:schemas.Contact, id, db: Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    contact_edit = db.query(models.Contact).filter(models.Contact.id == id)
    if contact_edit.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with {id} does not exist")
    else:
        contact_edit.update({models.Contact.email:request.email, models.Contact.phone:request.phone, models.Contact.linkedIn_URL:request.linkedIn_URL}, synchronize_session=False)
        # save the changes
        db.commit()
   
    return {"message": "Contact Updated sucessful"}


@router.delete('/delete/')
def delete_all(db:Session = Depends(get_db), admin_id = Depends(token_gen.get_verify_user_token)):
    all_contact = db.query(models.Contact)
    if all_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Contacts")
    all_contact.delete()
    db.commit()
    return {"message": "Contact deleted successfully"}
