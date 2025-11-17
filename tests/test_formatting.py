import unittest
from dataoperator.dataoperator import DataOperator


class TestFormattingMethods(unittest.TestCase):
    """Tests for formatting methods: firstname, lastname, state, and country"""
    
    # ===== format_person_firstname tests =====
    
    def test_format_person_firstname_simple_lowercase(self):
        """Test simple lowercase name conversion"""
        lod = [{'firstname': 'joe'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Joe')
    
    def test_format_person_firstname_simple_uppercase(self):
        """Test simple uppercase name conversion"""
        lod = [{'firstname': 'JOE'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Joe')
    
    def test_format_person_firstname_unicode_escape(self):
        """Test Unicode escape sequence conversion"""
        lod = [{'firstname': 'JosU+00E9'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'José')
    
    def test_format_person_firstname_unicode_escape_umlaut(self):
        """Test Unicode escape sequence with umlaut"""
        lod = [{'firstname': 'JU+00FCrgen'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Jürgen')

    def test_format_person_firstname_unicode_escape_umlaut2(self):
        lod = [{'firstname': 'bjU+00F6rn'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Björn')
    
    def test_format_person_firstname_hyphenated(self):
        """Test hyphenated name conversion"""
        lod = [{'firstname': 'ANNE-MARIE'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Anne-Marie')
    
    def test_format_person_firstname_chinese_chars(self):
        """Test that Chinese characters are not modified"""
        lod = [{'firstname': '李明'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], '李明')
    
    def test_format_person_firstname_japanese_chars(self):
        """Test that Japanese characters are not modified"""
        lod = [{'firstname': 'さくら'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'さくら')
    
    def test_format_person_firstname_empty_string(self):
        """Test with empty string"""
        lod = [{'firstname': ''}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], '')
    
    def test_format_person_firstname_none_value(self):
        """Test with None value"""
        lod = [{'firstname': None}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], None)
    
    # ===== format_person_lastname tests =====
    
    def test_format_person_lastname_simple_uppercase(self):
        """Test simple uppercase lastname"""
        lod = [{'lastname': 'FUSARO'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'Fusaro')
    
    def test_format_person_lastname_simple_lowercase(self):
        """Test simple lowercase lastname"""
        lod = [{'lastname': 'whiteman'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'Whiteman')
    
    def test_format_person_lastname_mc_prefix(self):
        """Test Mc prefix (McCormick)"""
        lod = [{'lastname': 'MCCORMICK'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'McCormick')
    
    def test_format_person_lastname_mac_prefix(self):
        """Test Mac prefix (MacDonald)"""
        lod = [{'lastname': 'MACDONALD'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'MacDonald')
    
    def test_format_person_lastname_van_compound(self):
        """Test Van compound name"""
        lod = [{'lastname': 'VANECK'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'VanEck')
    
    def test_format_person_lastname_van_der_multiword(self):
        """Test multi-word Van der surname"""
        lod = [{'lastname': 'van der sar'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'Van Der Sar')
    
    def test_format_person_lastname_apostrophe(self):
        """Test O'Malley apostrophe name"""
        lod = [{'lastname': "O'MALLEY"}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], "O'Malley")
    
    def test_format_person_lastname_empty_string(self):
        """Test with empty string"""
        lod = [{'lastname': ''}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], '')
    
    # ===== format_state_territory_iso2 tests =====
    
    def test_format_state_territory_iso2_new_york_proper(self):
        """Test 'new york' -> 'NY'"""
        lod = [{'state': 'new york'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'NY')
    
    def test_format_state_territory_iso2_nueva_york(self):
        """Test Spanish 'nueva york' -> 'NY'"""
        lod = [{'state': 'nueva york'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'NY')
    
    def test_format_state_territory_iso2_chinese_new_york(self):
        """Test Chinese '紐約' -> 'NY'"""
        lod = [{'state': '紐約'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'NY')
    
    def test_format_state_territory_iso2_american_samoa(self):
        """Test 'American Samoa' -> 'AS'"""
        lod = [{'state': 'American Samoa'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'AS')
    
    def test_format_state_territory_iso2_guam_uppercase(self):
        """Test 'GUAM' -> 'GU'"""
        lod = [{'state': 'GUAM'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'GU')
    
    def test_format_state_territory_iso2_us_minor_outlying_islands(self):
        """Test 'United States Minor Outlying Islands' -> 'UM'"""
        lod = [{'state': 'United States Minor Outlying Islands'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'UM')
    
    def test_format_state_territory_iso2_us_minor_outlying_islands_typo(self):
        """Test misspelling 'United State Minor Outlying Islands' -> 'UM'"""
        lod = [{'state': 'United State Minor Outlying Islands'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'UM')
    
    def test_format_state_territory_iso2_new_yrk_misspelling(self):
        """Test misspelling 'new yrk' -> 'NY'"""
        lod = [{'state': 'new yrk'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="state",
            operator="format_state_territory_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['state'], 'NY')
    
    # ===== format_country_iso2 tests =====
    
    def test_format_country_iso2_armenia_lowercase(self):
        """Test 'armenia' -> 'AM'"""
        lod = [{'country': 'armenia'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'AM')
    
    def test_format_country_iso2_turkey(self):
        """Test 'Turkey' -> 'TR'"""
        lod = [{'country': 'Turkey'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'TR')
    
    def test_format_country_iso2_turkiye(self):
        """Test 'Turkiye' -> 'TR'"""
        lod = [{'country': 'Turkiye'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'TR')
    
    def test_format_country_iso2_turkiye_umlaut(self):
        """Test 'Türkiye' -> 'TR'"""
        lod = [{'country': 'Türkiye'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'TR')
    
    def test_format_country_iso2_republic_of_turkiye(self):
        """Test 'The Republic of Turkiye' -> 'TR'"""
        lod = [{'country': 'The Republic of Turkiye'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'TR')
    
    def test_format_country_iso2_usa_abbrev(self):
        """Test 'USA' -> 'US'"""
        lod = [{'country': 'USA'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'US')
    
    def test_format_country_iso2_usa_abbrev_dots(self):
        """Test 'U.S.A.' -> 'US'"""
        lod = [{'country': 'U.S.A.'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'US')
    
    def test_format_country_iso2_untied_states_typo(self):
        """Test misspelling 'Untied States of America' -> 'US'"""
        lod = [{'country': 'Untied States of America'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'US')
    
    def test_format_country_iso2_deutschland(self):
        """Test 'deutschland' -> 'DE'"""
        lod = [{'country': 'deutschland'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'DE')
    
    def test_format_country_iso2_germany_uppercase(self):
        """Test 'GERMANY' -> 'DE'"""
        lod = [{'country': 'GERMANY'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'DE')
    
    def test_format_country_iso2_germany_chinese_traditional(self):
        """Test Chinese '德國' -> 'DE'"""
        lod = [{'country': '德國'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'DE')
    
    def test_format_country_iso2_china_simplified(self):
        """Test Chinese '中国' -> 'CN'"""
        lod = [{'country': '中国'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'CN')
    
    def test_format_country_iso2_china_traditional(self):
        """Test Chinese '中國' -> 'CN'"""
        lod = [{'country': '中國'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'CN')
    
    def test_format_country_iso2_colombia(self):
        """Test 'Colombia' -> 'CO'"""
        lod = [{'country': 'Colombia'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'CO')
    
    def test_format_country_iso2_columbia_misspelling(self):
        """Test common misspelling 'Columbia' -> 'CO'"""
        lod = [{'country': 'Columbia'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso2"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'CO')
    
    # ===== format_country_iso3 tests =====
    
    def test_format_country_iso3_armenia(self):
        """Test 'armenia' -> 'ARM'"""
        lod = [{'country': 'armenia'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso3"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'ARM')
    
    def test_format_country_iso3_usa(self):
        """Test 'USA' -> 'USA'"""
        lod = [{'country': 'USA'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso3"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'USA')
    
    def test_format_country_iso3_germany(self):
        """Test 'Germany' -> 'DEU'"""
        lod = [{'country': 'Germany'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso3"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'DEU')
    
    def test_format_country_iso3_china(self):
        """Test 'China' -> 'CHN'"""
        lod = [{'country': 'China'}]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="country",
            operator="format_country_iso3"
        )
        result = op.execute()
        self.assertEqual(result[0]['country'], 'CHN')
    
    # ===== Multiple records tests =====
    
    def test_format_firstname_multiple_records(self):
        """Test formatting multiple records at once"""
        lod = [
            {'firstname': 'joe'},
            {'firstname': 'JANE'},
            {'firstname': 'ANNE-MARIE'}
        ]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="firstname",
            operator="format_person_firstname"
        )
        result = op.execute()
        self.assertEqual(result[0]['firstname'], 'Joe')
        self.assertEqual(result[1]['firstname'], 'Jane')
        self.assertEqual(result[2]['firstname'], 'Anne-Marie')
    
    def test_format_lastname_multiple_records(self):
        """Test formatting multiple records at once"""
        lod = [
            {'lastname': 'FUSARO'},
            {'lastname': 'MCCORMICK'},
            {'lastname': 'VANECK'}
        ]
        op = DataOperator(
            field_type="string",
            operator_type="format_value",
            lod=lod,
            field="lastname",
            operator="format_person_lastname"
        )
        result = op.execute()
        self.assertEqual(result[0]['lastname'], 'Fusaro')
        self.assertEqual(result[1]['lastname'], 'McCormick')
        self.assertEqual(result[2]['lastname'], 'VanEck')


if __name__ == '__main__':
    unittest.main()
