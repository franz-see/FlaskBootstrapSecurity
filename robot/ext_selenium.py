from Selenium2Library import Selenium2Library 

# Note : regenerate using https://github.com/robotframework/RIDE/wiki/Keyword-Completion

class CustomSelenium2Library(Selenium2Library):

    def get_all_text(self, locator):
        found_elements = self._element_find(locator, False, False)
        elements = found_elements if isinstance(found_elements, list) else [found_elements]
        return [element.text for element in elements]

    def element_attribute_should_be(self, locator, expected_value):
        actual_value = self._get_element_attribute(locator, expected_value)
        if actual_value != expected_value:
            raise AssertionError("Element Attribute %s should have been %s but was %s." % (locator, expected_value, actual_value))

    def element_attribute_should_not_be(self, locator, expected_value):
        actual_value = self._get_element_attribute(locator, expected_value)
        if actual_value == expected_value:
            raise AssertionError("Element Attribute %s should NOT have been %s but was %s." % (locator, expected_value, actual_value))

    def _get_element_attribute(self, locator, expected_value):
        return self.get_element_attribute(locator)
