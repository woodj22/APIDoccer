from string import Template
from pkg_resources import resource_string
from .php_parser import PHPTransformerParser


class Swagger:
    def __init__(self, path, model_name):
        self.model_name = model_name
        self.parser = PHPTransformerParser()

        self.content = self.get_content_from_transformer(path)

    @classmethod
    def get_content_from_transformer(cls, path):
        with open(path) as f:
            lines = f.readlines()
        return [x.strip().strip(',') for x in lines]

    def map_casts_to_model_attributes(self):

        map_array = self.parser.get_transformer_array(self.content, "public $map", False)
        casts_array = self.parser.get_transformer_array(self.content,  "public $casts", True)

        return self.parser.map_casts_to_values(map_array, casts_array)

    def create_swagger_definition(self):

        resource = resource_string(__name__, 'data/swagger_definition.txt')
        swagger_template = Template(resource)
        casted_attributes = self.map_casts_to_model_attributes()
        swagger_properties = self.create_swagger_properties(casted_attributes)
        includes = self.create_available_includes()
        details = {
            'modelName': self.model_name,
            'modelPluralName': 'people',
            'properties': ''.join(swagger_properties),
            'availableIncludes': ''.join(includes)
        }

        return swagger_template.substitute(details)

    def create_available_includes(self):
        available_includes = self.parser.get_transformer_array(self.content, "protected $availableIncludes", False)

        return [self.make_swagger_include_property(include) for include in available_includes]

    def create_swagger_properties(self, casted_attributes):

        return [self.make_swagger_property(attribute, cast) for [attribute, cast] in casted_attributes]

    @staticmethod
    def split_transform_array(array, delimiter=" => ", keep_values=True):
        if keep_values:
            return dict(key.split(delimiter) for key in array)
        else:
            return [key.split(delimiter)[0] for key in array]

    @staticmethod
    def make_swagger_property(attribute, cast):
        return " *     @SWG\Property(property = " + attribute + ",          type =" + cast + ", default = ''), \n"

    def make_swagger_include_property(self, reference_name):
        return " *     @SWG\Property(property = " + reference_name + ", type = 'array',@SWG\Items(ref='#/definitions/"+reference_name+"'),),\n"
