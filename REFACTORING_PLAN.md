# FLEXT-WEB REFACTORING PLAN

## Module Structure Changes

### Current → New Module Names (PEP8 Compliant)
- `config.py` → `config.py` ✓ (already compliant)
- `services.py` → `service.py` (singular, following flext-core pattern)
- `models.py` → `model.py` (singular)
- `handlers.py` → `handler.py` (singular)
- `exceptions.py` → `exception.py` (singular)
- `fields.py` → `field.py` (singular)
- `protocols.py` → `protocol.py` (singular)
- `typings.py` → `type.py` (shorter, following flext-core pattern)
- `interfaces.py` → REMOVE (duplicate of protocols)
- `type_aliases.py` → REMOVE (merge into type.py)
- `utilities.py` → `util.py` (shorter)
- `constants.py` → REMOVE (move to flext-core or local constants)

### Consolidated Classes Structure (Following Flext-Core Pattern)

#### 1. FlextWebConfig (config.py)
- Single class with nested Config classes
- Extends flext-core configuration patterns

#### 2. FlextWebService (service.py) 
- Single class extending FlextDomainService
- Contains nested WebService, AppManager, etc.
- No separate FlextWebServices wrapper

#### 3. FlextWebModel (model.py)
- Single class extending FlextModels patterns
- Contains nested App, AppStatus, Handler classes
- Follows consolidated model pattern

#### 4. FlextWebField (field.py)
- Single class extending FlextFields
- All web-specific validators and fields

#### 5. FlextWebException (exception.py)
- Single class extending FlextExceptions
- Hierarchy of web-specific exceptions

### Files to Remove/Merge
- `interfaces.py` → Remove (duplicate of protocols)
- `type_aliases.py` → Merge into `type.py`
- `legacy.py` → Remove (no longer needed)
- `utilities.py` → Merge core utils into respective modules

### Centralization Strategy
- **Types**: Keep web-specific types, move generic ones to flext-core
- **Constants**: Move generic constants to flext-core, keep web-specific ones
- **Base Classes**: Use flext-core bases, no local abstractions
- **Protocols**: Keep web-specific protocols, remove duplicates

### Quality Requirements
- 100% ruff compliance (no noqa)
- 100% mypy/pyright compliance (no type: ignore)
- 100% test coverage with functional tests
- All imports from flext-core root level
- No circular dependencies
- No legacy compatibility layers