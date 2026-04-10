from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.repositories.permission import PermissionRepository
from app.schemas.permission import Permission, PermissionCreate, RolePermissionCreate
from app.schemas.user import Role
from app.core.dependencies import get_current_admin_user

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.get("", response_model=List[Permission])
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Получить все разрешения (только админ)"""
    from sqlalchemy import select
    from app.models.user import Permission
    
    result = await db.execute(select(Permission).order_by(Permission.resource))
    return result.scalars().all()


@router.post("", response_model=Permission, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_in: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Создать разрешение (только админ)"""
    from app.models.user import Permission
    
    # Проверяем, существует ли уже такое разрешение
    from sqlalchemy import select
    result = await db.execute(
        select(Permission).where(
            Permission.resource == permission_in.resource,
            Permission.action == permission_in.action,
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission already exists",
        )
    
    permission = Permission(**permission_in.model_dump())
    db.add(permission)
    await db.flush()
    await db.refresh(permission)
    
    return permission


@router.get("/roles", response_model=List[Role])
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Получить все роли (только админ)"""
    from sqlalchemy import select
    from app.models.user import Role
    
    result = await db.execute(select(Role).order_by(Role.name))
    return result.scalars().all()


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: Role,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Создать роль (только админ)"""
    from app.models.user import Role
    
    # Проверяем, существует ли уже такая роль
    from sqlalchemy import select
    result = await db.execute(select(Role).where(Role.name == role_in.name))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists",
        )
    
    role = Role(**role_in.model_dump(exclude={'id', 'created_at', 'updated_at'}))
    db.add(role)
    await db.flush()
    await db.refresh(role)
    
    return role


@router.post("/roles/{role_id}/assign")
async def assign_permissions_to_role(
    role_id: int,
    permission_ids: list[int],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Назначить разрешения роли (только админ)"""
    from app.models.user import RolePermission
    from sqlalchemy import delete
    
    # Удаляем старые разрешения
    await db.execute(
        delete(RolePermission).where(RolePermission.role_id == role_id)
    )
    
    # Добавляем новые
    for perm_id in permission_ids:
        role_perm = RolePermission(role_id=role_id, permission_id=perm_id)
        db.add(role_perm)
    
    await db.flush()
    
    return {"message": "Permissions assigned successfully"}


@router.get("/roles/{role_id}", response_model=Role)
async def get_role_with_permissions(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """Получить роль с разрешениями (только админ)"""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.user import Role, RolePermission, Permission
    
    result = await db.execute(
        select(Role)
        .options(selectinload(Role.permissions).selectinload(RolePermission.permission))
        .where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    
    return role
