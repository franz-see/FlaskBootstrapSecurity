from Selenium2Library import Selenium2Library 

# Note : regenerate using https://github.com/robotframework/RIDE/wiki/Keyword-Completion

class CustomSelenium2Library(Selenium2Library):

    def get_all_text(self, locator):
        found_elements = self._element_find(locator, False, False)
        elements = found_elements if isinstance(found_elements, list) else [found_elements]
        return [element.text for element in elements]

