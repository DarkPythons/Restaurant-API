from fastapi import APIRouter, Depends, HTTPException, status, Response
from .utils import get_current_user
from auth.models import User
from typing import Annotated
from .schemas import AddNewCourierShemas

orders_router = APIRouter()

