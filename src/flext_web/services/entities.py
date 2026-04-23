"""Entity service for flext-web."""

from __future__ import annotations

import uuid
from collections.abc import (
    MutableMapping,
    Sequence,
)

from flext_web import m, p, r, s, u


class FlextWebEntities(s[bool]):
    """In-memory entity CRUD support for flext-web."""

    _storage: MutableMapping[str, m.Web.EntityData] = u.PrivateAttr(
        default_factory=lambda: dict[str, m.Web.EntityData](),
    )

    def create(self, data: m.Web.EntityData) -> p.Result[m.Web.EntityData]:
        """Create an entity with generated identifier."""
        entity_id = str(uuid.uuid4())
        entity = m.Web.EntityData(data={"id": entity_id, **data.data})
        self._storage[entity_id] = entity
        return r[m.Web.EntityData].ok(entity)

    def execute(
        self,
    ) -> p.Result[bool]:
        """Execute the entity namespace service."""
        return r[bool].ok(True)

    def fetch_entity(self, entity_id: str) -> p.Result[m.Web.EntityData]:
        """Fetch an entity by identifier."""
        if not u.to_str(entity_id):
            return r[m.Web.EntityData].fail("Entity ID cannot be empty")
        entity = self._storage.get(entity_id)
        if entity is None:
            return r[m.Web.EntityData].fail(f"Entity not found: {entity_id}")
        return r[m.Web.EntityData].ok(entity)

    def list_all(self) -> p.Result[Sequence[m.Web.EntityData]]:
        """List all registered entities."""
        return r[Sequence[m.Web.EntityData]].ok(list(self._storage.values()))

    def validate_business_rules(self) -> p.Result[bool]:
        """Validate entity namespace invariants."""
        return r[bool].ok(True)


__all__: list[str] = ["FlextWebEntities"]
