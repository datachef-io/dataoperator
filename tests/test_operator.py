import unittest
from src.dataoperator import DataOperator


class TestDataOperator(unittest.TestCase):
    
    def test_init_valid(self):
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
        self.assertEqual(operator.field_type, "number")
        self.assertEqual(operator.operator_type, "merge_values")

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
        
        # # Test with numeric values
        # lod = [{"id": 1}, {"id": 2}, {"id": 3}]
        # operator = cls(
        #     field_type="number", 
        #     operator_type="merge_values", 
        #     lod=lod, 
        #     field="id", 
        #     operator="concatenate_all_values"
        # )
        
        # self.assertEqual(operator.concatenate_all_values(), "1|2|3")
        
        # Test with mixed values
        # lod = [{"value": "abc"}, {"value": 123}, {"value": True}]
        # operator = cls(
        #     field_type="mixed", 
        #     operator_type="merge_values", 
        #     lod=lod, 
        #     field="value", 
        #     operator="concatenate_all_values"
        # )
        
        # self.assertEqual(operator.concatenate_all_values(), "abc|123|True")
        
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
            field="age", 
            operator="keep_record_with_newest_value",
            datetime_field="created_at"
        )
        
        records = operator.execute()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Bob")
        self.assertEqual(records[0]["created_at"], "2023-01-03T12:00:00")
        
        # Test with missing datetime_field
        operator = DataOperator(
            field_type="datetime", 
            operator_type="select_master_record", 
            lod=lod, 
            field="age", 
            operator="keep_record_with_newest_value"
        )
        
        with self.assertRaises(AssertionError):
            operator.keep_record_with_newest_value()
            
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
            field="age", 
            operator="keep_record_with_newest_value",
            datetime_field="created_at"
        )
        
        records = operator.keep_record_with_newest_value()
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
            field="age", 
            operator="keep_record_with_newest_value",
            datetime_field="created_at"
        )
        
        records = operator.keep_record_with_newest_value()
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


if __name__ == '__main__':
    unittest.main()