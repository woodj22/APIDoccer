

class PHPTransformerParser:

    @staticmethod
    def find_transformer_array_lines(transformer_text, array_name):
        found_start = False
        start_point = 0
        end_point = 0

        for index, line in enumerate(transformer_text):
            if array_name in line:
                start_point = index + 1
                found_start = True
            if found_start and "];" in line:
                end_point = index
                break

        return transformer_text[start_point:end_point]

    @staticmethod
    def map_array_lines_to_array(line_array, delimiter=" => ", keep_values=True):
        if keep_values:
            return dict(key.split(delimiter) for key in line_array)
        else:
            return [key.split(delimiter)[0] for key in line_array]

    def get_transformer_array(self, transformer_string_text, array_name, keep_values):
        line_array = self.find_transformer_array_lines(transformer_text=transformer_string_text, array_name=array_name)
        return self.map_array_lines_to_array(line_array, keep_values=keep_values)

    @staticmethod
    def map_casts_to_values(transformer_map, cast_map):
        return [[key, cast_map[key]] if key in cast_map.keys() else [key, "'string'"] for key in transformer_map]
