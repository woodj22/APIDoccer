from string import Template
from pkg_resources import resource_string


class Swagger:
    def __init__(self, path, model_name):
        self.transformerFilePath = path
        self.model_name = model_name
        self.content = self.get_content_from_transformer()

    def get_content_from_transformer(self):
        with open(self.transformerFilePath) as f:
            lines = f.readlines()
        return [x.strip().strip(',') for x in lines]

    def map_model_attributes(self):
        map_array = "public $map"
        i = self.get_transformer_array(self.content, map_array)
        cast_array = "public $casts"
        casts = self.get_transformer_array(self.content, cast_array)
        d = self.map_to_casts(self.split_transform_array(i, keep_values=False), self.split_transform_array(casts))
        return self.map_to_swagger_property(self.content[i[0]:i[1]])

    def get_transformer_array(self, transformer, array_name):
        found_start = False
        start_point = 0
        end_point = 0

        for index, line in enumerate(transformer):
            if array_name in line:
                start_point = index + 1
                found_start = True
            if found_start and "];" in line:
                end_point = index
                break

        return transformer[start_point:end_point]

    def create_swagger_definition(self):
        swagger_template = resource_string(__name__, 'data/swagger_definition.txt')
        src = Template(swagger_template)
        properties = self.map_model_attributes()
        details = {
            'modelName': self.model_name,
            'modelPluralName': 'people',
            'properties': ''.join(properties)
        }

        return src.substitute(details)
    # (property name => type)
    def map_to_swagger_property(self, transformer_array):

        return [self.make_property(name) for name in transformer_array]

    def map_to_casts(self, transformer_map, cast_map):

        d = [[key, value] if key in transformer_map else [key, 'string'] for (key, value) in cast_map]
        exit(d)
        for key, value in cast_map:
            if key in transformer_map:

                transformer_map[:] = [key, value]
            else:
                transformer_map[:] = 'string'

        exit(transformer_map)
        return transformer_map

    @staticmethod
    def split_transform_array(array, delimiter=" => ", keep_values=True):
        if keep_values:
            return [key.split(delimiter) for key in array]
        else:
            return [key.split(delimiter)[0] for key in array]



    @staticmethod
    def make_property(name):
        return " *     @SWG\Property(property = " + name.split("=>")[0]+ ",          type = 'string', default = ''), \n"