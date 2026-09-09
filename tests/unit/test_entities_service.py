"""Unit tests for flext_web entity service."""

from __future__ import annotations

from flext_tests import tm

from flext_web import FlextWebEntities, m


class TestsFlextWebEntities:
    """Test suite for FlextWebEntities."""

    def test_create_entity(self) -> None:
        """Entity service creates an entity with generated id."""
        service = FlextWebEntities()
        data = m.Web.EntityData(data={"name": "Test Entity"})
        result = service.create(data)
        tm.ok(result)
        tm.that(result.value.data, has="id")
        tm.that(result.value.data["name"], eq="Test Entity")

    def test_execute(self) -> None:
        """Entity service execute returns success."""
        service = FlextWebEntities()
        result = service.execute()
        tm.ok(result)
        tm.that(result.value is True, eq=True)

    def test_fetch_entity_success(self) -> None:
        """Entity service fetches a created entity."""
        service = FlextWebEntities()
        data = m.Web.EntityData(data={"name": "Test Entity"})
        created = service.create(data)
        tm.ok(created)
        entity_id = str(created.value.data["id"])
        result = service.fetch_entity(entity_id)
        tm.ok(result)
        tm.that(result.value.data["name"], eq="Test Entity")

    def test_fetch_entity_empty_id(self) -> None:
        """Entity service rejects empty identifier."""
        service = FlextWebEntities()
        result = service.fetch_entity("")
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_fetch_entity_not_found(self) -> None:
        """Entity service fails for unknown identifier."""
        service = FlextWebEntities()
        result = service.fetch_entity("nonexistent-id")
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_list_all(self) -> None:
        """Entity service lists all created entities."""
        service = FlextWebEntities()
        data = m.Web.EntityData(data={"name": "List Entity"})
        tm.ok(service.create(data))
        result = service.list_all()
        tm.ok(result)
        tm.that(len(result.value), eq=1)

    def test_validate_business_rules(self) -> None:
        """Entity service validates business rules."""
        service = FlextWebEntities()
        result = service.validate_business_rules()
        tm.ok(result)
        tm.that(result.value is True, eq=True)
