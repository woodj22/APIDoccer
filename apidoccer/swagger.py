from string import Template
from pkg_resources import resource_string, resource_filename
from .php_parser import PHPTransformerParser


class Swagger(PHPTransformerParser):
    def __init__(self, **definition):
        self.model_name = definition.get('model_name')
        self.plural_model_name = definition.get('plural_model_name')

    @classmethod
    def map_transformer_to_array(cls, path):
        with open(path) as f:
            lines = f.readlines()
        return [x.strip().strip(',') for x in lines]

    @staticmethod
    def add_values_to_template(resource_name, substitute_values):
        resource = resource_string(__name__, resource_name)
        swagger_template = Template(resource.decode('utf-8'))
        return swagger_template.safe_substitute(substitute_values)

    def create_index_function(self, path):
        details = {
            'path': path,
            'modelPluralName': self.plural_model_name,
            'tag': 'People'
        }
        return self.add_values_to_template('data/swagger_index_function_block.txt', details)

    def create_swagger_definition(self, transformer_path):

        transformer_string = self.map_transformer_to_array(transformer_path)
        swagger_properties = self.create_swagger_properties(self.map_casts_to_model_attributes(transformer_string))
        includes = self.create_available_includes(transformer_string)
        details = {
            'modelName': self.model_name,
            'modelPluralName': self.plural_model_name,
            'properties': ''.join(swagger_properties),
            'availableIncludes': ''.join(includes)
        }

        return self.add_values_to_template('data/swagger_definition.txt', details)

    def create_available_includes(self, transformer_string):
        available_includes = self.get_transformer_array(transformer_string, "protected $availableIncludes", False)

        return [self.make_swagger_include_property(include) for include in available_includes]

    def create_swagger_properties(self, casted_attributes):

        return [self.make_swagger_property(attribute, cast) for [attribute, cast] in casted_attributes]

    @staticmethod
    def make_swagger_property(attribute, cast):
        return " *     @SWG\Property(property = " + attribute + ",          type =" + cast + ", default = ''), \n"

    @staticmethod
    def make_swagger_include_property(reference_name):
        return " *     @SWG\Property(property = " + reference_name + ", type = 'array',@SWG\Items(ref='#/definitions/"+reference_name+"'),),\n"
