from string import Template
from pkg_resources import resource_string
from .php_parser import PHPTransformerParser

class Swagger:
    def __init__(self, path, model_name):
        self.model_name = model_name
        self.content = self.get_content_from_transformer(path)

    @classmethod
    def get_content_from_transformer(cls, path):
        with open(path) as f:
            lines = f.readlines()
        return [x.strip().strip(',') for x in lines]

    def map_model_attributes(self):

        parser = PHPTransformerParser()
        map_array = parser.get_transformer_array(self.content, "public $map", False)
        casts_array = parser.get_transformer_array(self.content,  "public $casts", True)

        return parser.map_casts_to_values(map_array, casts_array)

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



    @staticmethod
    def split_transform_array(array, delimiter=" => ", keep_values=True):
        if keep_values:
            return dict(key.split(delimiter) for key in array)
        else:
            return [key.split(delimiter)[0] for key in array]



    @staticmethod
    def make_property(name):
        return " *     @SWG\Property(property = " + name.split("=>")[0]+ ",          type = 'string', default = ''), \n"