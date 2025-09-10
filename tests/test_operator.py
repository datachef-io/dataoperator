import unittest
from dataoperator.dataoperator import DataOperator

REAL_LOD_A = [
    {
        'annualrevenue': '',
        'billingcity': 'Auckland',
        'billingcountry': 'New Zealand',
        'billingpostalcode': '1010',
        'billingstate': '', 
        'billingstreet': '21 Industrial St', 
        'createdbyid': '00544000009RQ1zAAG',
        'createddate': '2019-02-07T02:11:42',
        'description': 'Managed IT Services and IT Support for small businesses.', 
        'id': '001440000244mnfAAA', 
        'industry': '', 
        'isdeleted': False, 
        'lastmodifieddate': '2025-09-02T17:31:52', 
        'name': 'QQQ Corp', 
        'numberofemployees': '', 
        'ownerid': '245', 
        'phone': '', 
        'systemmodstamp': '2025-09-02T17:31:52', 
        'type': '', 
        'website': 'www.qqq.com'
    }, 
    {
        'annualrevenue': 5012438.0, 
        'billingcity': 'NORCROSS', 
        'billingcountry': 'United States', 
        'billingpostalcode': '30092-3677', 
        'billingstate': 'Georgia',
        'billingstreet': '5875 INDUSTRIAL BLVD # 10', 
        'createdbyid': '005E0000004xFZRIA2', 
        'createddate': '2014-04-10T15:32:35', 
        'description': 'Up and coming IT company.', 
        'industry': 'Technology', 
        'isdeleted': False, 
        'lastmodifieddate': '2025-07-28T20:29:14', 
        'name': 'QQQ Corporation', 
        'numberofemployees': 25.0, 
        'ownerid': '987', 
        'phone': '+1.555.633.2551', 
        'systemmodstamp': '2025-07-28T20:29:14', 
        'type': 'Prospect', 
        'website': 'https://qqq.com'
    }
]


class TestDataOperator(unittest.TestCase):
    
    def test_init_valid_number_field_type(self):
        """Test valid initialization of BaseOperator"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        operator = DataOperator(
            field_type="number", 
            operator_type="merge_values", 
            lod=lod, 
            field="age", 
            operator="keep_max_value"
        )
        self.assertEqual(operator.lod, lod)
        self.assertEqual(operator.field,    "age")
        self.assertEqual(operator.operator, "keep_max_value")
        self.assertEqual(operator.field_type, "int") # mapped from "number"
        self.assertEqual(operator.operator_type, "merge_values")

    def test_init_valid_address_field_type(self):
        """Test valid initialization of BaseOperator"""
        lod = [
            {"name": "John", "age": 30, "address": "1 Smith St"},
            {"name": "Jane", "age": 25, "address": "2 Oak St"}
        ]
        operator = DataOperator(
            field_type="address", 
            operator_type="merge_values", 
            lod=lod, 
            field="address", 
            operator="keep_newest_value"
        )
        self.assertEqual(operator.lod, lod)
        self.assertEqual(operator.field,    "address")
        self.assertEqual(operator.operator, "keep_newest_value")
        self.assertEqual(operator.field_type, "string") # mapped from "address"
        self.assertEqual(operator.operator_type, "merge_values")

    def test_init_with_all_fields(self):
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="Name",
            operator="CONCATENATE_ALL_VALUES",
            datetime_field="Created_At",
            value="Joe",
            lod=[{"name": "Joe"}]
        )
        assert op.field == "name"
        assert op.operator == "concatenate_all_values"
        assert op.datetime_field == "created_at"
        assert op.value == "Joe"

    def test_init_with_missing_kwargs(self):
        op = DataOperator(
            field_type="string",
            operator_type="merge_values"
            # No field, operator, datetime_field, value, or lod
        )
        assert op.field is None
        assert op.operator is None
        assert op.datetime_field is None
        assert op.value is None

    def test_init_invalid_operator_type(self):
        """Test initialization with invalid operator_type"""
        with self.assertRaises(AssertionError):
            DataOperator(
                field_type="number", 
                operator_type="invalid_type", 
                lod=[{"name": "John", "age": 30}], 
                field="age", 
                operator="keep_max_value"
            )

    def test_init_invalid_lod_type(self):
        """Test initialization with invalid lod type"""
        with self.assertRaises(AssertionError):
            DataOperator(
                field_type="number", 
                operator_type="merge_values", 
                lod="not a list", 
                field="age", 
                operator="keep_max_value"
            )

    def test_init_invalid_lod_elements(self):
        """Test initialization with invalid lod elements"""
        with self.assertRaises(AssertionError):
            DataOperator(
                field_type="number", 
                operator_type="merge_values", 
                lod=[1, 2, 3], 
                field="age", 
                operator="keep_max_value"
            )

    def test_init_missing_field(self):
        """Test initialization with missing field in dictionaries"""
        with self.assertRaises(AssertionError):
            DataOperator(
                field_type="number", 
                operator_type="merge_values", 
                lod=[{"name": "John"}, {"name": "Jane"}], 
                field="age", 
                operator="keep_max_value"
            )

    def test_init_datetime_field_required(self):
        """Test initialization with datetime operators but missing datetime_field"""
        lod = [{"name": "John", "age": 30, "created_at": "2023-01-01T12:00:00"}, 
               {"name": "Jane", "age": 25, "created_at": "2023-01-02T12:00:00"}]
        with self.assertRaises(AssertionError):
            DataOperator(
                field_type="datetime", 
                operator_type="merge_values", 
                lod=lod, 
                field="name", 
                operator="KEEP_RECENT_VALUE"
            )

    def test_concatenate_all_values(self):
        """Test concatenate_all_values method"""
        # Test with string values
        lod = [{"name": "John"}, {"name": "Jane"}, {"name": "Bob"}]
        operator = DataOperator(
            field_type="string", 
            operator_type="merge_values", 
            lod=lod, 
            field="name", 
            operator="concatenate_all_values"
        )
        
        self.assertEqual(operator.concatenate_all_values(), "John|Jane|Bob")
        
        # Test with empty list
        lod = []
        operator = DataOperator(
            field_type="string", 
            operator_type="merge_values", 
            lod=lod, 
            field="name", 
            operator="concatenate_all_values"
        )
        self.assertRaises(AssertionError, operator.concatenate_all_values)
        
        # Test with single item
        lod = [{"name": "John"}]
        operator = DataOperator(
            field_type="string", 
            operator_type="merge_values", 
            lod=lod, 
            field="name", 
            operator="concatenate_all_values"
        )
        self.assertEqual(operator.concatenate_all_values(), "John")
        
        # Test with None values - should ignore None values
        lod = [{"name": "John"}, {"name": None}, {"name": "Jane"}, {"name": None}, {"name": "Bob"}]
        operator = DataOperator(
            field_type="string", 
            operator_type="merge_values", 
            lod=lod, 
            field="name", 
            operator="concatenate_all_values"
        )
        
        self.assertEqual(operator.concatenate_all_values(), "John|Jane|Bob")
        
        # Test with all None values - should return empty string
        lod = [{"name": None}, {"name": None}, {"name": None}]
        operator = DataOperator(
            field_type="string", 
            operator_type="merge_values", 
            lod=lod, 
            field="name", 
            operator="concatenate_all_values"
        )
        
        self.assertEqual(operator.concatenate_all_values(), None)

    def test_keep_oldest_value_created_at(self):
        lod = [
            {"name": "Alice", "created_at": "2022-01-01T12:00:00"},
            {"name": "Bob",   "created_at": "2021-01-01T12:00:00"},
            {"name": "Carol", "created_at": "2023-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_oldest_value",
            datetime_field="created_at",
            lod=lod
        )
        assert op.keep_oldest_value() == "Bob"

    def test_keep_newest_value_created_at(self):
        lod = [
            {"name": "Alice", "created_at": "2022-01-01T12:00:00"},
            {"name": "Bob",   "created_at": "2021-01-01T12:00:00"},
            {"name": "Carol", "created_at": "2023-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_newest_value",
            datetime_field="created_at",
            lod=lod
        )
        assert op.keep_newest_value() == "Carol"

    def test_keep_oldest_value_specify_datetime_field(self):
        lod = [
            {"name": "Alice", "dt_x": "2022-01-01T12:00:00"},
            {"name": "Bob",   "dt_x": "2021-01-01T12:00:00"},
            {"name": "Carol", "dt_x": "2023-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_oldest_value",
            datetime_field="dt_x",
            lod=lod
        )
        assert op.keep_oldest_value() == "Bob"

    def test_keep_newest_value_specify_datetime_field(self):
        lod = [
            {"name": "Alice", "dt_x": "2022-01-01T12:00:00"},
            {"name": "Bob",   "dt_x": "2021-01-01T12:00:00"},
            {"name": "Carol", "dt_x": "2023-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_newest_value",
            datetime_field="dt_x",
            lod=lod
        )
        assert op.keep_newest_value() == "Carol"

    def test_keep_oldest_value_createddate_autodetect(self):
        lod = [
            {"name": "Alice", "createddate": "2022-01-01T12:00:00"},
            {"name": "Bob",   "createddate": "2021-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_oldest_value",
            lod=lod
        )
        assert op.keep_oldest_value() == "Bob"

    def test_keep_newest_value_createdat_autodetect(self):
        lod = [
            {"name": "Alice", "createdat": "2022-01-01T12:00:00"},
            {"name": "Bob",   "createdat": "2023-01-01T12:00:00"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="name",
            operator="keep_newest_value",
            lod=lod
        )
        assert op.keep_newest_value() == "Bob"

    def test_keep_max_value(self):
        """Test keep_max_value method"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="merge_values", 
            lod=lod, 
            field="age", 
            operator="keep_max_value"
        )
        
        self.assertEqual(operator.keep_max_value(), 35)

    def test_keep_min_value(self):
        """Test keep_min_value method"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="merge_values", 
            lod=lod, 
            field="age", 
            operator="keep_min_value"
        )
        
        self.assertEqual(operator.keep_min_value(), 25)

    def test_keep_max_value_when_all_values_are_none(self):
        """Test initialization when all values in the field are None"""
        lod = [{"id": "001111", "annualrevenue": None}, {"id": "001222", "annualrevenue": ''}]
        operator = DataOperator(
            field_type="currency", 
            operator_type="merge_values", 
            lod=lod, 
            field="annualrevenue", 
            operator="keep_max_value"
        )
        result = operator.execute()
        self.assertEqual(result, None)

    def test_keep_max_value_when_string_values_in_field(self):
        """Test initialization when some values in the field are strings"""

        operator = DataOperator(
            field_type="currency", 
            operator_type="merge_values", 
            lod=REAL_LOD_A, 
            field="annualrevenue", 
            operator="keep_max_value"
        )
        result = operator.execute()
        self.assertEqual(result, 5012438.0)

    def test_keep_record_with_max_value(self):
        """Test keep_record_with_max_value method"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="select_master_record", 
            lod=lod, 
            field="age", 
            operator="keep_record_with_max_value"
        )
        
        records = operator.keep_record_with_max_value()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Bob")
        self.assertEqual(records[0]["age"], 35)
        
        # Test with multiple records having the same max value
        lod = [{"name": "John", "age": 35}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="select_master_record", 
            lod=lod, 
            field="age", 
            operator="keep_record_with_max_value"
        )
        
        records = operator.keep_record_with_max_value()
        self.assertEqual(len(records), 2)
        self.assertTrue(any(r["name"] == "John" for r in records))
        self.assertTrue(any(r["name"] == "Bob" for r in records))

    def test_keep_record_with_min_value(self):
        """Test keep_record_with_min_value method"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="select_master_record", 
            lod=lod, 
            field="age", 
            operator="keep_record_with_min_value"
        )
        
        records = operator.execute()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Jane")
        self.assertEqual(records[0]["age"], 25)

    def test_keep_record_with_newest_value(self):
        """Test keep_record_with_newest_value method"""
        lod = [
            {"name": "John", "age": 30, "created_at": "2023-01-01T12:00:00"}, 
            {"name": "Jane", "age": 25, "created_at": "2023-01-02T12:00:00"}, 
            {"name": "Bob", "age": 35, "created_at": "2023-01-03T12:00:00"}
        ]
        operator = DataOperator(
            field_type="datetime", 
            operator_type="select_master_record", 
            lod=lod, 
            field="created_at", 
            operator="keep_record_with_newest_value",
        )
        
        records = operator.execute()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Bob")
        self.assertEqual(records[0]["created_at"], "2023-01-03T12:00:00")
            
        # Test with None datetime values
        lod = [
            {"name": "John", "age": 30, "created_at": None}, 
            {"name": "Jane", "age": 25, "created_at": "2023-01-02T12:00:00"}, 
            {"name": "Bob", "age": 35, "created_at": "2023-01-03T12:00:00"}
        ]
        operator = DataOperator(
            field_type="datetime", 
            operator_type="select_master_record", 
            lod=lod, 
            field="created_at", 
            operator="keep_record_with_newest_value",
        )
        
        records = operator.execute()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Bob")
        
        # Test with multiple records having the same newest datetime
        lod = [
            {"name": "John", "age": 30, "created_at": "2023-01-03T12:00:00"}, 
            {"name": "Jane", "age": 25, "created_at": "2023-01-02T12:00:00"}, 
            {"name": "Bob", "age": 35, "created_at": "2023-01-03T12:00:00"}
        ]
        operator = DataOperator(
            field_type="datetime", 
            operator_type="select_master_record", 
            lod=lod, 
            field="created_at", 
            operator="keep_record_with_newest_value",
        )
        
        records = operator.execute()
        self.assertEqual(len(records), 2)
        self.assertTrue(any(r["name"] == "John" for r in records))
        self.assertTrue(any(r["name"] == "Bob" for r in records))

    def test_greater_than(self):
        """Test greater_than method"""
        operator = DataOperator(
            field_type="number", 
            operator_type="evaluate_condition", 
            field="age", 
            operator="greater_than",
            value=25
        )
        
        # Set up a record for testing
        operator.record = {"name": "John", "age": 30}
        self.assertTrue(operator.greater_than())
        
        # Test with value greater than field
        operator.value = 35
        self.assertFalse(operator.greater_than())
        
        # Test with non-numeric field
        operator.record = {"name": "John", "age": "thirty"}
        with self.assertRaises(AssertionError):
            operator.greater_than()

    def test_less_than(self):
        """Test less_than method"""
        operator = DataOperator(
            field_type="number", 
            operator_type="evaluate_condition", 
            field="age", 
            operator="less_than",
            value=35
        )
        
        # Set up a record for testing
        operator.record = {"name": "John", "age": 30}
        self.assertTrue(operator.less_than())
        
        # Test with value less than field
        operator.value = 25
        self.assertFalse(operator.less_than())
        
        # Test with non-numeric field
        operator.record = {"name": "John", "age": "thirty"}
        with self.assertRaises(AssertionError):
            operator.less_than()

    def test_execute(self):
        """Test execute method"""
        lod = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}]
        operator = DataOperator(
            field_type="number", 
            operator_type="merge_values", 
            lod=lod, 
            field="age", 
            operator="keep_max_value"
        )
        
        self.assertEqual(operator.execute(), 35)
        
        # Test with different operator
        operator.operator = "keep_min_value"
        self.assertEqual(operator.execute(), 25)

    def test_keep_true_value(self):
        """Test keep_true_value method"""
        # Test with all True values
        lod = [{"active": True}, {"active": True}, {"active": True}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_true_value"
        )
        
        self.assertTrue(operator.keep_true_value())
        
        # Test with mixed boolean values (some True, some False)
        lod = [{"active": False}, {"active": True}, {"active": False}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_true_value"
        )
        
        self.assertTrue(operator.keep_true_value())
        
        # Test with all False values
        lod = [{"active": False}, {"active": False}, {"active": False}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_true_value"
        )
        
        self.assertIsNone(operator.keep_true_value())
        
        # Test with truthy/falsy values (not strictly boolean)
        lod = [{"status": 0}, {"status": ""}, {"status": 1}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="status", 
            operator="keep_true_value"
        )
        self.assertTrue(operator.keep_true_value())
        
        # Test with all falsy values
        lod = [{"status": 0}, {"status": ""}, {"status": None}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="status", 
            operator="keep_true_value"
        )
        
        self.assertIsNone(operator.keep_true_value())
        
        # Test with empty list
        lod = []
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_true_value"
        )
        
        self.assertRaises(AssertionError, operator.keep_true_value)

    def test_keep_false_value(self):
        """Test keep_false_value method"""
        # Test with all False values
        lod = [{"active": False}, {"active": False}, {"active": False}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_false_value"
        )
        
        self.assertFalse(operator.keep_false_value())
        
        # Test with mixed boolean values (some True, some False)
        lod = [{"active": False}, {"active": True}, {"active": False}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_false_value"
        )
        
        self.assertFalse(operator.keep_false_value())
        
        # Test with all True values
        lod = [{"active": True}, {"active": True}, {"active": True}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_false_value"
        )
        
        self.assertIsNone(operator.keep_false_value())
        
        # Test with truthy/falsy values (not strictly boolean)
        lod = [{"status": 0}, {"status": ""}, {"status": None}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="status", 
            operator="keep_false_value"
        )
        
        self.assertFalse(operator.keep_false_value())
        
        # Test with mixed truthy/falsy values
        lod = [{"status": 0}, {"status": ""}, {"status": 1}]
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="status", 
            operator="keep_false_value"
        )
        
        self.assertFalse(operator.keep_false_value())
        
        # Test with empty list
        lod = []
        operator = DataOperator(
            field_type="boolean", 
            operator_type="merge_values", 
            lod=lod, 
            field="active", 
            operator="keep_false_value"
        )
        
        self.assertRaises(AssertionError, operator.keep_false_value)

    def test_preserve_priority_returns_first_match(self):
        lod = [
            {"status": "B"},
            {"status": "C"},
            {"status": "D"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="status",
            operator="preserve_priority",
            value=["A", "B", "C", "D"],
            lod=lod
        )
        assert op.preserve_priority() == "B"

    def test_preserve_priority_returns_none_if_no_match(self):
        lod = [
            {"status": "X"},
            {"status": "Y"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="status",
            operator="preserve_priority",
            value=["A", "B", "C", "D"],
            lod=lod
        )
        assert op.preserve_priority() is None

    def test_preserve_priority_with_different_field(self):
        lod = [
            {"priority": "low"},
            {"priority": "medium"},
            {"priority": "high"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="priority",
            operator="preserve_priority",
            value=["high", "medium", "low"],
            lod=lod
        )
        assert op.preserve_priority() == "high"

    def test_preserve_priority_asserts_on_nonlist_value(self):
        lod = [
            {"status": "A"},
        ]
        op = DataOperator(
            field_type="string",
            operator_type="merge_values",
            field="status",
            operator="preserve_priority",
            value="A",  # Not a list!
            lod=lod
        )
        try:
            op.preserve_priority()
            assert False, "Should have raised AssertionError"
        except AssertionError:
            pass

    def test_keep_corporate_domain(self):
        lod = [
            {"id": "001", "email": "jose.conseco@gmail.com"},
            # {"id": "002", "email": "jose.conseco@10minutemail.com"},
            {"id": "004", "email": "jose.conseco@yahoo.com"},
            {"id": "005", "email": "jose.conseco@example.org"},
            {"id": "006", "email": "jose.conseco@mailinator.com"},
            {"id": "007", "email": "jose.conseco@bigcorp.co"},
        ]
        operator = DataOperator(
            field_type="email", 
            lod=lod,
            field="email",
            operator_type="merge_values",
            operator="keep_corporate_domain"
        )
        result = operator.execute()
        assert result == "jose.conseco@example.org"

if __name__ == '__main__':
    unittest.main()