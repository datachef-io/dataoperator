import inspect
from datetime import datetime

from dataoperator.free_email_domains import FREE_EMAIL_DOMAINS
from dataoperator.disposable_email_domains import DISPOSABLE_EMAIL_DOMAINS

METHODS_BY_OPERATOR_TYPE = {
    'evaluate_condition': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'greater_than',
        'less_than',
    ],
    'update_field': [
        'set_string',
        'set_true',
        'set_false',
        # 'increment',
        # 'decrement',
    ],
    'merge_values': [
        'keep_true_value',
        'keep_false_value',
        'keep_max_value',
        'keep_min_value',
        'keep_newest_value',
        'keep_oldest_value',
        'preserve_priority',
        'concatenate_all_values',
        'keep_corporate_domain',
    ],
    'select_master_record': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_record_with_max_value',
        'keep_record_with_min_value',
        'keep_record_with_newest_value',
        'keep_record_with_oldest_value',
        'keep_record_with_highest_priority'
    ],
}

METHODS_BY_FIELD_TYPE = {
    'id': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
    ],
    'boolean': [
        'keep_true_value',
        'keep_false_value',
        'set_true',
        'set_false',
    ],
    'string': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'concatenate_all_values',
        'preserve_priority',
        'set_string',
    ],
    'email': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'keep_corporate_domain',
        'set_string',
    ],
    'text': [
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'concatenate_all_values',
        'set_string',
    ],
    'multipicklist': [
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'concatenate_all_values',
    ],
    'picklist': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'preserve_priority',
        'set_string',
    ],
    'int': [
        # 'equals',
        # 'not_equals',
        'greater_than',
        'less_than',
        'keep_max_value',
        'keep_min_value',
        'keep_newest_value',
        'keep_oldest_value',
        'keep_record_with_max_value',
        'keep_record_with_min_value',
        # 'increment',
        # 'decrement',
    ],
    'date': [
        'keep_newest_value',
        'keep_oldest_value',
        'keep_record_with_newest_value',
        'keep_record_with_oldest_value',
    ],
    'phone': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
    ],
    'url': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
    ],
}

FIELD_TYPE_MAP = {
    'reference': 'id',
    'number': 'int',
    'double': 'int',
    'float': 'int',
    'percent': 'int',
    'currency': 'int',
    'integer': 'int',
    'address': 'string',
    'combobox': 'string',
    'datetime': 'date',
    'textarea': 'text',
}


class DataOperator:

    def __init__(self, field_type: str, operator_type: str, **kwargs):
        """

        Acceptable kwargs:
        - lod: list of dictionaries; each dictionary represents a "record"; e.g. [{"id": "a", "name": "joe"}, {"id": "b", "name": "jane"}]
        - field: the field to apply the operator to; e.g. "name", "age", "numberofemployees"
        - operator: the operator to apply; e.g. "contains", "greater_than", "max"
        - datetime_field: the field to use for datetime comparison; e.g. "created_at"
        - value: the value to compare against; e.g. "joe"

        NOTE: Joins and aggregations should take place _before_ this step. In other words, tables should be joined and aggregations 
        should be fed into `lod` with the aggregation as its own column. Then evaluation can take place as if these were any
        regular column.
        """
        if field_type.lower() == 'id':
            field_type = 'id'
        elif field_type.lower() == 'email':
            field_type = 'email'
        elif field_type not in METHODS_BY_FIELD_TYPE:
            field_type = FIELD_TYPE_MAP.get(field_type, field_type)

        assert operator_type in list(METHODS_BY_OPERATOR_TYPE.keys()), f"Invalid operator_type: {operator_type}; must be one of {list(METHODS_BY_OPERATOR_TYPE.keys())}"
        assert field_type in list(METHODS_BY_FIELD_TYPE.keys()), f"Invalid field_type: {field_type}; must be one of {list(METHODS_BY_FIELD_TYPE.keys())}"

        self.field_type = field_type
        self.operator_type = operator_type

        self.lod = kwargs.get('lod')
        self.field = kwargs.get('field').lower() if kwargs.get('field') else None
        self.operator = kwargs.get('operator').lower() if kwargs.get('operator') else None # e.g. "greater_than", "max", "keep_recent_value", "keep_oldest_value", "preserve_priority"
        self.datetime_field = kwargs.get('datetime_field').lower() if kwargs.get('datetime_field') else None
        self.value = kwargs.get('value', None)

        if self.lod:
            assert self.field, "'field' is a required kwarg when 'lod' is provided"
            assert isinstance(self.lod, list)
            assert all(isinstance(record, dict) for record in self.lod)
        
        if self.lod and self.operator_type != 'update_field':
            assert all(self.field in d for d in self.lod), f"Field '{self.field}' not found in all dictionaries"
            
            # Evaluate condition operations should only work with single records
            if self.operator_type == 'evaluate_condition':
                assert len(self.lod) == 1, "evaluate_condition operations require exactly one record in lod"

        if self.operator:
            # assert self.field, "'field' is a required kwarg when 'operator' is provided"
            assert self.operator in METHODS_BY_OPERATOR_TYPE[self.operator_type], f"Invalid operator: {self.operator}; must be one of {list(METHODS_BY_OPERATOR_TYPE[self.operator_type])}"
            assert self.operator in METHODS_BY_FIELD_TYPE[self.field_type], f"Invalid operator: {self.operator}; must be one of {list(METHODS_BY_FIELD_TYPE[self.field_type])}"

        # if self.operator in ('KEEP_RECENT_VALUE', 'KEEP_OLDEST_VALUE'):
        #     assert self.datetime_field, "'datetime_field' is a required kwarg when using KEEP_RECENT_VALUE or KEEP_OLDEST_VALUE operator"

    def _get_created_datetime_field(self):
        if self.datetime_field:
            return self.datetime_field
        elif "createddate" in self.lod[0]:
            return "createddate"
        elif "created_at" in self.lod[0]:
            return "created_at"
        elif "createdat" in self.lod[0]:
            return "createdat"
        else:
            raise ValueError("No datetime field found")

    def get_methods(self):
        return [
            method_name for method_name, method in inspect.getmembers(self, predicate=inspect.isroutine) 
            if not method_name.startswith("__")
            and method_name not in ('execute', 'get_methods')
            and method_name in METHODS_BY_OPERATOR_TYPE[self.operator_type]
            and method_name in METHODS_BY_FIELD_TYPE[self.field_type]
            ]

    def execute(self):
        _method = getattr(self, self.operator.lower())
        try:
            return _method()
        except Exception as e:
            raise e

    # shared or base components
    def common_assert_number(self):
        assert type(self.record[self.field]) in (int, float), "Field must be a number for condition operator"

    def common_assert_lod(self):
        assert self.lod, "lod is required for this method"

    def at_least_one_value_in_lod_for_field(self):
        self.common_assert_lod()
        return True if any(d[self.field] not in ['', None] for d in self.lod) else False

    def greater_than(self):
        self.common_assert_number()
        return self.record[self.field] > self.value

    def less_than(self):
        self.common_assert_number()
        return self.record[self.field] < self.value

    def _min_value(self):
        return min(d[self.field] for d in self.lod)

    def _max_value(self):
        return max(d[self.field] for d in self.lod)

    # Evaluate conditions
    def equals(self) -> bool:
        self.common_assert_lod()
        return self.lod[0][self.field] == self.value

    def not_equals(self) -> bool:
        self.common_assert_lod()
        return self.lod[0][self.field] != self.value

    def contains(self) -> bool:
        self.common_assert_lod()
        return self.value.lower() in self.lod[0][self.field].lower()

    def not_contains(self) -> bool:
        self.common_assert_lod()
        return self.value.lower() not in self.lod[0][self.field].lower()

    # Set values
    def set_string(self):
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item:
                item[self.field] = self.value
        return self.lod

    def set_true(self):
        assert self.field_type == 'boolean'
        pass

    def set_false(self):
        assert self.field_type == 'boolean'
        pass


    # Deduplication -> surviving record methods
    def keep_record_with_max_value(self) -> list:
        """
        Among 2 or more records, return the record which has the maximum value for the given field.
        """
        self.common_assert_lod()
        max_value = self._max_value()
        records = [d for d in self.lod if d[self.field] == max_value]
        return records

    def keep_record_with_min_value(self) -> list:
        self.common_assert_lod()
        min_value = self._min_value()
        records = [d for d in self.lod if d[self.field] == min_value]
        return records

    def keep_record_with_newest_value(self) -> list:
        self.common_assert_lod()
        
        # Convert datetime strings to datetime objects for comparison
        max_datetime = max(
            datetime.fromisoformat( d[self.field] ) 
            for d in self.lod
            if d[self.field] not in ['', None]
        )
        
        # Find the record(s) that match max_datetime
        records = [
            d for d in self.lod 
            if d[self.field] not in ['', None]
            and datetime.fromisoformat(d[self.field]) == max_datetime
        ]
        
        return records

    def keep_record_with_oldest_value(self) -> list:
        """ TODO FIXME - refactor so that oldest and newest can share code """

        self.common_assert_lod()
        
        # Convert datetime strings to datetime objects for comparison
        min_datetime = min(
            datetime.fromisoformat(d[self.field]) 
            for d in self.lod
            if d[self.field] not in ['', None]
        )
        
        # Find the record(s) that match min_datetime
        records = [
            d for d in self.lod 
            if d[self.field] not in ['', None]
            and datetime.fromisoformat(d[self.field]) == min_datetime
        ]
        
        return records

    # Deduplication -> field merge methods
    def keep_oldest_value(self) -> str:
        self.common_assert_lod()
        datetime_field = self._get_created_datetime_field()
        min_datetime = min(
            datetime.fromisoformat(d[datetime_field]) 
            for d in self.lod
            if d[datetime_field] is not None
        )
        # get the record in lod that has the min_datetime
        record = [
            d for d in self.lod 
            if d[datetime_field] not in ['', None]
            and datetime.fromisoformat(d[datetime_field]) == min_datetime
        ][0]
        return record[self.field]

    def keep_newest_value(self) -> str:
        self.common_assert_lod()
        datetime_field = self._get_created_datetime_field()
        max_datetime = max(
            datetime.fromisoformat(d[datetime_field]) 
            for d in self.lod
            if d[datetime_field] not in ['', None]
        )
        # get the record in lod that has the max_datetime
        record = [
            d for d in self.lod
            if d[datetime_field] not in ['', None]
            and datetime.fromisoformat(d[datetime_field]) == max_datetime
        ][0]
        return record[self.field]

    def keep_max_value(self) -> int:
        if self.at_least_one_value_in_lod_for_field():
            return max(d[self.field] for d in self.lod if isinstance(d[self.field], (int, float)))

    def keep_min_value(self) -> int:
        if self.at_least_one_value_in_lod_for_field():
            return min(d[self.field] for d in self.lod if isinstance(d[self.field], (int, float)))

    def concatenate_all_values(self) -> str:
        self.common_assert_lod()
        if self.at_least_one_value_in_lod_for_field():
            return "|".join(str(d[self.field]) for d in self.lod if d[self.field] not in ['', None])

    def keep_true_value(self) -> bool:
        """ if any record has True for the given field, return True """
        self.common_assert_lod()
        return True if any(d[self.field] for d in self.lod if isinstance(d[self.field], (bool, int))) == True else None

    def keep_false_value(self) -> bool:
        """ if any record has False for the given field, return False """
        self.common_assert_lod()
        if self.at_least_one_value_in_lod_for_field():
            return False if any(d[self.field] for d in self.lod if isinstance(d[self.field], (bool, int))) == False else None

    def preserve_priority(self) -> str:
        """
        in this context, self.value must contain a list 
        of values in the order of priority

        e.g. ['A', 'B', 'C', 'D']
        if any record has 'A' for the given field, return 'A'
        if any record has 'B' for the given field, return 'B'
        etc.
        """
        self.common_assert_lod()
        assert type(self.value) == list

        for value in self.value:
            for record in self.lod:
                if record[self.field] == value:
                    return value
        return None

    def keep_corporate_domain(self) -> str:  
        """ 
        TODO FIXME - this will always return the first record's domain if there are multiple 
        corporate domains; there should be some additional logic to handle cases where there
        are multiple corporate domains (e.g. email validation, comparison with other fields in
        the record, etc.)
        """
        self.common_assert_lod()
        return [
            d[self.field] for d in self.lod 
            if d[self.field].split("@")[1] not in FREE_EMAIL_DOMAINS 
            and d[self.field].split("@")[1] not in DISPOSABLE_EMAIL_DOMAINS
            ][0]