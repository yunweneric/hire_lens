"""
Base CRUD service for HireLens MVC architecture.

Models define data structure; services own persistence and business rules;
views/controllers delegate to services and render templates or API responses.
"""
from __future__ import annotations

from abc import ABC
from typing import Any, Generic, TypeVar

from django.db import models
from django.db.models import QuerySet

T = TypeVar("T", bound=models.Model)


class BaseCRUDService(ABC, Generic[T]):
    """Abstract base service providing standard database CRUD operations."""

    model: type[T]

    def get_queryset(self) -> QuerySet[T]:
        return self.model.objects.all()

    def get_by_id(self, pk: int) -> T:
        return self.get_queryset().get(pk=pk)

    def get_or_none(self, pk: int) -> T | None:
        return self.get_queryset().filter(pk=pk).first()

    def list(self, **filters: Any) -> QuerySet[T]:
        qs = self.get_queryset()
        if filters:
            qs = qs.filter(**filters)
        return qs

    def create(self, **data: Any) -> T:
        return self.model.objects.create(**data)

    def update(self, instance: T, **data: Any) -> T:
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()

    def delete_by_id(self, pk: int) -> bool:
        deleted, _ = self.model.objects.filter(pk=pk).delete()
        return deleted > 0

    def count(self, **filters: Any) -> int:
        return self.list(**filters).count()

    def exists(self, **filters: Any) -> bool:
        return self.list(**filters).exists()
