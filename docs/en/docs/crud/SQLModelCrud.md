## SQLModelSelector

- SQLModel selector

### fields

#### model

- Current SQLModel ORM model, must be set.

#### fields

Query field list.

- Support SQLModel model field, SQLModel model, current model database table field name
- Support current model fields, and other model fields.
- Default: `self.model`

#### exclude

A list of excluded fields. A list of fields to exclude from the current model.

- Support current SQLModel model field, current model database table field name
- Default: []

#### ordering

- Selector to sort field list.
- Default: []

#### link_models

- Link model dictionary. It is more complicated, and the detailed analysis needs to be improved.

#### pk_name

- current model primary key string, default: `id`.
- Description: **Database table has and can only have one self-incrementing primary key**. (To be expanded)

#### pk

- The current model primary key sqlalchemy InstrumentedAttribute.

#### parser

- The current model field resolver.
- Reference: `SQLModelFieldParser`

#### _list_fields_ins

- Batch query sqlalchemy field list.

### method:

#### get_select

- Returns the SQLModel selector.

```python
def get_select(self, request: Request) -> Select
```

#### calc_filter_clause

- Calculate query filter conditions.

```python
def calc_filter_clause(
    self,
    data: Dict[str, Any]
) -> List[BinaryExpression]
```

## SQLModelCrud

- SQLModel ORM Crud Registrar

### Inherit from base class

- #### [BaseCrud](../BaseCrud/#basecrud)

- #### [SQLModelSelector](#sqlmodelselector)

### fields

#### engine

- sqlalchemy connection engine, must be set.

#### readonly_fields

Read-only field list:

- Support SQLModel model field, SQLModel model, current model database table field name
- Support current model fields, and other model fields.
- Default: `[]`

### method:

#### get_select

- Returns the SQLModel selector.

```python
def get_select(self, request: Request) -> Select
```

#### on_create_pre

- Returns the processed data of the create request.

```python
async def on_create_pre(
    self,
    request: Request,
    obj: SchemaCreateT,
    **kwargs
) -> Dict[str, Any]
```

#### on_update_pre

- Returns the data after the update request has been processed.

```python
async def on_update_pre(
    self,
    request: Request,
    obj: SchemaUpdateT,
    item_id: Union[List[str], List[int]],
    **kwargs
) -> Dict[str, Any]
```

#### on_filter_pre

- Returns the data processed by the batch query request submission filter.

```python
async def on_filter_pre(
    self,
    request: Request,
    obj: SchemaFilterT,
    **kwargs
) -> Dict[str, Any]
```
