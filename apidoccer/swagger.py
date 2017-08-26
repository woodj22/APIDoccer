from string import Template
from pkg_resources import resource_string
from .php_parser import PHPTransformerParser


class Swagger:
    def __init__(self, transformer_path, **definition):

        self.model_name = definition.get('model_name')
        self.plural_model_name = definition.get('plural_model_name')
        self.parser = PHPTransformerParser()
        self.content = self.get_content_from_transformer(transformer_path)

    @classmethod
    def get_content_from_transformer(cls, path):
        with open(path) as f:
            lines = f.readlines()
        return [x.strip().strip(',') for x in lines]

    # def set_swagger_details(self, detail_input):
    #    return self.details = detail_input
    #

    def map_casts_to_model_attributes(self):

        map_array = self.parser.get_transformer_array(self.content, "public $map", False)
        casts_array = self.parser.get_transformer_array(self.content,  "public $casts", True)

        return self.parser.map_casts_to_values(map_array, casts_array)

    @staticmethod
    def add_values_to_template(resource_name, substitute_values):
        resource = resource_string(__name__, resource_name)
        swagger_template = Template(resource)

        return swagger_template.substitute(substitute_values)

    def create_swagger_definition(self):

        casted_attributes = self.map_casts_to_model_attributes()
        swagger_properties = self.create_swagger_properties(casted_attributes)
        includes = self.create_available_includes()
        details = {
            'modelName': self.model_name,
            'modelPluralName': self.plural_model_name,
            'properties': ''.join(swagger_properties),
            'availableIncludes': ''.join(includes)
        }

        return self.add_values_to_template('data/swagger_definition.txt', details)

    def create_available_includes(self):
        available_includes = self.parser.get_transformer_array(self.content, "protected $availableIncludes", False)

        return [self.make_swagger_include_property(include) for include in available_includes]

    def create_swagger_properties(self, casted_attributes):

        return [self.make_swagger_property(attribute, cast) for [attribute, cast] in casted_attributes]

    @staticmethod
    def make_swagger_property(attribute, cast):
        return " *     @SWG\Property(property = " + attribute + ",          type =" + cast + ", default = ''), \n"

    @staticmethod
    def make_swagger_include_property(reference_name):
        return " *     @SWG\Property(property = " + reference_name + ", type = 'array',@SWG\Items(ref='#/definitions/"+reference_name+"'),),\n"
