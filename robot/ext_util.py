# Note : regenerate using https://github.com/robotframework/RIDE/wiki/Keyword-Completion
from datetime import datetime

class CustomUtilLibrary:

    def combine_by_columns(self, *args):
        combined = []
        if not len(args):
            return combined

        shapes = [len(arg) for arg in args]
        message = "All lists must have the same shape, but got %s." % ','.join([str(s) for s in shapes])
        assert len(set(shapes)) == 1, message

        length = len(args[0])
        for i in range(length):
            combined.append(tuple([arg[i] for arg in args]))

        return combined

    def split_by_columns(self, to_be_split):
        list_of_columns = []
        for row in to_be_split:
            for i, cell in enumerate(row):
                if i >= len(list_of_columns):
                    list_of_columns.insert(i, [])
                list_of_columns[i].append(cell)
        return [tuple(column) for column in list_of_columns]

    def convert_date_format(self, input_date_str, from_format, to_format):
        originally_a_list = isinstance(input_date_str, list)
        originally_a_tuple = isinstance(input_date_str, tuple)
        sources = input_date_str if originally_a_list or originally_a_tuple else [input_date_str]
        converted_values = []
        for source in sources:
            converted_values.append(datetime.strptime(source, from_format).strftime(to_format))

        if originally_a_list:
            return converted_values
        elif originally_a_tuple:
            return tuple(converted_values)
        else:
            return converted_values[0]

            
