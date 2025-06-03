# DataOperator

DataOperator is a base level class for Datachef record processing. It includes methods for parsing one or more records and determining the final value for a given field based on the operator.

This README file was written with AI so it may not be 100% accurate. Please refer to the source code for the most up to date information.

## Installation

``` TODO ```

## Usage

### Get All Available Methods

```python
from src.operator import DataOperator

operator = DataOperator()

print(operator.get_available_methods())
```

### Get Available Methods for a Specific Operator Type

```python
from src.operator import DataOperator

operator = DataOperator()

methods = operator.get_available_methods("merge_fields")

print(methods)
>>> ["concatenate_all_values", "keep_max_value", "keep_min_value", "keep_recent_value", "keep_oldest_value", "keep_corporate_domains", "preserve_priority"]
```

### Merge Fields

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="merge_fields", 
    lod=[{"name": "John"}, {"name": "Jane"}, {"name": "Bob"}], 
    field="name", 
    operator="concatenate_all_values"
)

result = operator.concatenate_all_values()

print(result)
>>> "John|Jane|Bob"
```

### Select Master Record

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="select_master_record", 
    lod=[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}], 
    field="age", 
    operator="keep_record_with_max_value"
)

result = operator.keep_record_with_max_value()

print(result)
>>> [{"name": "Bob", "age": 35}]
