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

        return [x.strip() for x in lines]

    def map_model_attributes(self):

        array_name = "public $map"
        i = self.get_array_index_points(self.content, array_name)
        return self.map_to_property(self.content[i[0]:i[1]])


    def get_array_index_points(self, transformer, array_name):
        found_start = False
        start_point = 0
        end_point = 0

        for index, line in enumerate(transformer):
            if array_name in line:
                start_point = index + 1
                found_start = True
            if found_start and "];" in line:
                end_point = index

        return start_point, end_point

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

    def map_to_property(self, transformer_array):
        return [self.make_property(name) for name in transformer_array]

    @staticmethod
    def make_property(name):
        return " *     @SWG\Property(property = " + name.split("=>")[0]+ ",          type = 'string', default = ''), \n"