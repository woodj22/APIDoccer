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

    def map_casts_to_model_attributes(self):

        parser = PHPTransformerParser()
        map_array = parser.get_transformer_array(self.content, "public $map", False)
        casts_array = parser.get_transformer_array(self.content,  "public $casts", True)

        return parser.map_casts_to_values(map_array, casts_array)


    def create_swagger_definition(self):
        swagger_template = resource_string(__name__, 'data/swagger_definition.txt')
        src = Template(swagger_template)
        casted_attributes = self.map_casts_to_model_attributes()
        swagger_properties = self.map_swagger_properties(casted_attributes)

        details = {
            'modelName': self.model_name,
            'modelPluralName': 'people',
            'properties': ''.join(swagger_properties)
        }

        return src.substitute(details)

    def map_swagger_properties(self, casted_attributes):

        return [self.make_swagger_property(attribute) for attribute in casted_attributes]

    @staticmethod
    def split_transform_array(array, delimiter=" => ", keep_values=True):
        if keep_values:
            return dict(key.split(delimiter) for key in array)
        else:
            return [key.split(delimiter)[0] for key in array]



    @staticmethod
    def make_swagger_property(attribute):
        return " *     @SWG\Property(property = " + attribute[0] + ",          type =" + attribute[1] + ", default = ''), \n"