from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from app import crud
from app.schemas import LinkCreate, LinkRead, LinkStats

router = APIRouter(
    prefix='/api/v1',
    tags=['shortener'],
)


@router.post('/links', response_model=LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db)):
    db_link = crud.create_link(db, link_in)
    return db_link

@router.get('/links', response_model=list[LinkRead])
def list_links(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    links = crud.list_links(db, limit=limit, offset=offset)
    return links

@router.get('/links/{short_code}', response_model=LinkStats)
def get_links_stats(short_code: str, db: Session = Depends(get_db)):
    link = crud.get_link_by_short_code(db, short_code)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    return LinkStats(
        short_code=link.short_code,
        long_url=link.long_url,
        click_count=link.click_count,
        is_active=link.is_active,
    )


@router.get("/{short_code}", include_in_schema=False)
def redirect_short_code(short_code: str, db: Session = Depends(get_db)):
    link = crud.get_link_by_short_code(db, short_code)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

    crud.increment_click_count(db, link)
    return RedirectResponse(url=link.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.delete('/links/{short_code}', status_code=status.HTTP_204_NO_CONTENT)
def delete_link(short_code: str, db: Session = Depends(get_db)):
    link = crud.soft_delete_link(db, short_code)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Link not found',
        )