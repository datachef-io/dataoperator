import inspect
import re
import unicodedata
from datetime import datetime

from dataoperator.free_email_domains import FREE_EMAIL_DOMAINS
from dataoperator.disposable_email_domains import DISPOSABLE_EMAIL_DOMAINS
from dataoperator.state_territory_mappings import STATE_TERRITORY_MAPPINGS, STATE_TERRITORY_VARIATIONS
from dataoperator.country_mappings import COUNTRY_MAPPINGS, COUNTRY_ABBREVIATIONS

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
        'append_string',
        'prepend_string',
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
    'match_condition': [
        'matches',
    ],
    'format_value': [
        'format_person_firstname',
        'format_person_lastname',
        'format_state_territory_iso2',
        'format_country_iso2',
        'format_country_iso3',
    ],
}

METHODS_BY_FIELD_TYPE = {
    'id': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'matches',
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
        'append_string',
        'prepend_string',
        'matches',
        'format_person_firstname',
        'format_person_lastname',
        'format_state_territory_iso2',
        'format_country_iso2',
        'format_country_iso3',
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
        'append_string',
        'prepend_string',
        'matches',
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
        'matches',
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
        'matches',
    ],
    'url': [
        'equals',
        'not_equals',
        'contains',
        'not_contains',
        'keep_newest_value',
        'keep_oldest_value',
        'matches',
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
        
        if self.lod and self.operator_type != "update_field":
            assert all(self.field in d for d in self.lod), f"Field '{self.field}' not found in all dictionaries"
            
        # Evaluate condition operations should only work with single records
        if self.lod and self.operator_type == "evaluate_condition":
            assert len(self.lod) == 1, "evaluate_condition operations require exactly one record in lod"

        if self.operator in ('set_true', 'set_false'):
            assert self.field_type == "boolean", f"{self.operator} can only be used when field_type = boolean"
            assert self.value is None, "value cannot be provided when using set_true or set_false operators"

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

    def _convert_keys_to_lowercase(self, original_dict):
        return dict((k.lower(), v) for k,v in original_dict.items())

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

    def matches(self):
        """ 
        This method is merely a placeholder, and must be implemented 
        upstream """
        raise NotImplementedError

    # Set values
    def set_string(self):
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item:
                item[self.field] = self.value
        return self.lod

    def append_string(self):
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item:
                existing_value = item[self.field] or ""
                item[self.field] = str(existing_value) + str(self.value)
        return self.lod

    def prepend_string(self):
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item:
                existing_value = item[self.field] or ""
                item[self.field] = str(self.value) + str(existing_value)
        return self.lod

    def set_true(self):
        assert self.field_type == 'boolean'
        for item in self.lod:
            if self.field in item:
                item[self.field] = True
        return self.lod

    def set_false(self):
        assert self.field_type == 'boolean'
        for item in self.lod:
            if self.field in item:
                item[self.field] = False
        return self.lod

    def format_person_firstname(self):
        """
        Format a person's first name to proper case.
        - Handles Unicode escape sequences (e.g., "U+00E9" -> "é")
        - Converts to proper case
        - Handles hyphenated names (e.g., "ANNE-MARIE" -> "Anne-Marie")
        - Excludes Chinese and Japanese characters from case processing
        """
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item and item[self.field]:
                name = str(item[self.field])
                
                # Replace Unicode escape sequences like "U+00E9" with actual Unicode characters
                name = self._replace_unicode_escapes(name)
                
                # Check if the name contains CJK (Chinese, Japanese, Korean) characters
                # If so, return as-is without case conversion
                if self._contains_cjk(name):
                    item[self.field] = name
                    continue
                
                # Convert to proper case, handling hyphens
                name = self._proper_case_name(name)
                
                item[self.field] = name
        return self.lod
    
    def format_person_lastname(self):
        """
        Format a person's last name to proper case with special handling for:
        - Prefixes: Mc, Mac (e.g., "MCCORMICK" -> "McCormick")
        - Compound names: Van, Von, De, etc. (e.g., "VANECK" -> "VanEck")
        - Apostrophes (e.g., "O'MALLEY" -> "O'Malley")
        - Multiple word surnames (e.g., "van der sar" -> "Van der Sar")
        """
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item and item[self.field]:
                name = str(item[self.field])
                
                # Apply lastname-specific formatting rules
                name = self._format_lastname(name)
                
                item[self.field] = name
        return self.lod
    
    def format_state_territory_iso2(self):
        """
        Format US state/territory names to ISO2 codes.
        - Handles exact matches
        - Handles misspellings via fuzzy matching
        - Handles multiple languages (Spanish, Chinese, etc.)
        """
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item and item[self.field]:
                input_value = str(item[self.field]).strip()
                
                # Try to find the ISO2 code
                iso2_code = self._lookup_state_territory(input_value)
                
                if iso2_code:
                    item[self.field] = iso2_code
        return self.lod
    
    def format_country_iso2(self):
        """
        Format country names to ISO2 codes.
        - Handles exact matches
        - Handles abbreviations (USA, U.S.A., etc.)
        - Handles misspellings via fuzzy matching
        - Handles multiple languages and aliases
        """
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item and item[self.field]:
                input_value = str(item[self.field]).strip()
                
                # Try to find the ISO2 code
                iso2_code = self._lookup_country(input_value, 'iso2')
                
                if iso2_code:
                    item[self.field] = iso2_code
        return self.lod
    
    def format_country_iso3(self):
        """
        Format country names to ISO3 codes.
        Similar to format_country_iso2 but returns ISO3 codes.
        """
        self.common_assert_lod()
        for item in self.lod:
            if self.field in item and item[self.field]:
                input_value = str(item[self.field]).strip()
                
                # Try to find the ISO3 code
                iso3_code = self._lookup_country(input_value, 'iso3')
                
                if iso3_code:
                    item[self.field] = iso3_code
        return self.lod
    
    # Helper methods for formatting
    
    def _replace_unicode_escapes(self, text):
        """Replace Unicode escape sequences like 'U+00E9' with actual Unicode characters."""
        # Pattern to match U+XXXX format
        pattern = r'U\+([0-9A-Fa-f]{4,6})'
        
        def replace_match(match):
            hex_code = match.group(1)
            try:
                # Convert hex string to integer and then to character
                return chr(int(hex_code, 16))
            except (ValueError, OverflowError):
                # If conversion fails, return original
                return match.group(0)
        
        return re.sub(pattern, replace_match, text)
    
    def _contains_cjk(self, text):
        """Check if text contains Chinese, Japanese, or Korean characters."""
        for char in text:
            # Check if character is in CJK Unicode ranges
            if '\u4e00' <= char <= '\u9fff' or \
               '\u3040' <= char <= '\u309f' or \
               '\u30a0' <= char <= '\u30ff' or \
               '\uac00' <= char <= '\ud7af':
                return True
        return False
    
    def _proper_case_name(self, name):
        """Convert name to proper case, handling hyphens and spaces."""
        if not name:
            return name
        
        # Split on hyphens and spaces
        parts = re.split(r'([-\s])', name)
        
        # Capitalize each part
        result = []
        for part in parts:
            if part in ['-', ' ']:
                result.append(part)
            elif part:
                # Capitalize first letter, lowercase rest
                result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
            else:
                result.append(part)
        
        return ''.join(result)
    
    def _format_lastname(self, name):
        """Format last name with special rules for prefixes and compound names."""
        if not name:
            return name
        
        # Normalize the name
        name = name.strip()
        
        # Handle special patterns
        
        # Pattern 1: Mc/Mac prefixes (e.g., "MCCORMICK" -> "McCormick", "MACDONALD" -> "MacDonald")
        if name.lower().startswith('mc') and len(name) > 2:
            return 'Mc' + name[2:].capitalize()
        
        if name.lower().startswith('mac') and len(name) > 3:
            # Check if it's likely a Mac prefix (not just starting with "mac")
            # Common Mac names: MacDonald, MacArthur, etc.
            # But not: Mack, Macon, etc.
            if len(name) > 4 and name[3].upper() != name[3].lower():  # Next char after 'mac' is a letter
                return 'Mac' + name[3:].capitalize()
        
        # Pattern 2: O' prefix (e.g., "O'MALLEY" -> "O'Malley")
        if name.lower().startswith("o'") and len(name) > 2:
            return "O'" + name[2:].capitalize()
        
        # Pattern 3: Multi-word surnames with Van, Von, De, etc.
        # (e.g., "van der sar" -> "Van der Sar", "VANECK" -> "VanEck")
        words = name.split()
        
        if len(words) > 1:
            # Multi-word surname
            result = []
            for i, word in enumerate(words):
                word_lower = word.lower()
                
                # Keep certain particles lowercase unless they're the first word
                if i > 0 and word_lower in ['van', 'von', 'de', 'der', 'den', 'di', 'da', 'le', 'la']:
                    result.append(word.capitalize())
                else:
                    result.append(word.capitalize())
            
            return ' '.join(result)
        
        # Pattern 4: Single word with Van/Von/De prefix (e.g., "VANECK" -> "VanEck")
        if name.lower().startswith('van') and len(name) > 3:
            # Check if rest starts with uppercase (indicating compound name)
            if len(name) > 4:
                rest = name[3:]
                return 'Van' + rest[0].upper() + rest[1:].lower()
        
        if name.lower().startswith('von') and len(name) > 3:
            if len(name) > 4:
                rest = name[3:]
                return 'Von' + rest[0].upper() + rest[1:].lower()
        
        # Default: simple proper case
        return self._proper_case_name(name)
    
    def _lookup_state_territory(self, input_value):
        """Look up state/territory ISO2 code from input string."""
        if not input_value:
            return None
        
        # Normalize input
        normalized = input_value.strip().lower()
        
        # Remove common punctuation
        normalized = normalized.replace('.', '').replace(',', '')
        
        # Try exact match in main mappings
        if normalized in STATE_TERRITORY_MAPPINGS:
            return STATE_TERRITORY_MAPPINGS[normalized]
        
        # Try exact match in variations
        if normalized in STATE_TERRITORY_VARIATIONS:
            return STATE_TERRITORY_VARIATIONS[normalized]
        
        # Try fuzzy matching for misspellings
        best_match = self._fuzzy_match(normalized, STATE_TERRITORY_MAPPINGS)
        if best_match:
            return STATE_TERRITORY_MAPPINGS[best_match]
        
        # If still no match, return None (or could return original)
        return None
    
    def _lookup_country(self, input_value, code_type='iso2'):
        """Look up country ISO code from input string."""
        if not input_value:
            return None
        
        # Normalize input
        normalized = input_value.strip().lower()
        
        # Remove common punctuation and extra spaces
        normalized = re.sub(r'[.,;]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Try exact match in main mappings
        if normalized in COUNTRY_MAPPINGS:
            return COUNTRY_MAPPINGS[normalized][code_type]
        
        # Try abbreviations (for iso2 only)
        if code_type == 'iso2' and normalized in COUNTRY_ABBREVIATIONS:
            return COUNTRY_ABBREVIATIONS[normalized]
        
        # Try fuzzy matching for misspellings
        best_match = self._fuzzy_match(normalized, COUNTRY_MAPPINGS)
        if best_match:
            return COUNTRY_MAPPINGS[best_match][code_type]
        
        # If still no match, return None
        return None
    
    def _fuzzy_match(self, query, mapping_dict, threshold=0.8):
        """
        Simple fuzzy matching using string similarity.
        Returns the best matching key from mapping_dict if similarity > threshold.
        """
        if not query:
            return None
        
        best_match = None
        best_score = 0
        
        for key in mapping_dict.keys():
            score = self._string_similarity(query, key)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = key
        
        return best_match
    
    def _string_similarity(self, s1, s2):
        """
        Calculate similarity between two strings using a simple algorithm.
        Returns a score between 0 and 1.
        """
        if not s1 or not s2:
            return 0
        
        if s1 == s2:
            return 1.0
        
        # Convert to lowercase for comparison
        s1 = s1.lower()
        s2 = s2.lower()
        
        # Calculate Levenshtein-like similarity
        # For simplicity, we'll use a character overlap ratio
        
        # Check if one string contains the other (high similarity)
        if s1 in s2 or s2 in s1:
            return 0.85
        
        # Count matching characters
        s1_chars = set(s1)
        s2_chars = set(s2)
        
        intersection = len(s1_chars & s2_chars)
        union = len(s1_chars | s2_chars)
        
        if union == 0:
            return 0
        
        # Jaccard similarity
        jaccard = intersection / union
        
        # Also consider length difference
        len_diff = abs(len(s1) - len(s2)) / max(len(s1), len(s2))
        len_similarity = 1 - len_diff
        
        # Weighted average
        return (jaccard * 0.6) + (len_similarity * 0.4)

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