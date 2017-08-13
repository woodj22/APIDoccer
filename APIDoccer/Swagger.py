from string import Template

class Swagger:
    def __init__(self, path, model_name):
        self.transformerFilePath = path
        self.model_name = model_name
        self.property_string = " *     @SWG\Property(property = 'distinguishedName', type = 'string', default = 'cn=blablabl,blalaldosooooo looong name'),"

    def map_model_transformer(self):
        with open(self.transformerFilePath) as f:
            lines = f.readlines()

        content = [x.strip() for x in lines]
        found_start = False
        start_point = 0
        end_point   = 0

        for index, line in enumerate(content):
            if "public $map" in line:
                start_point = index + 1
                found_start = True
            if found_start and "];" in line:
                end_point = index

        return self.get_input_names(content[start_point:end_point])

    def create_swagger_definition(self):
        filein = open('APIDoccer/swagger_definition.txt')
        src = Template(filein.read())
        properties = self.map_model_transformer()
        details = {'modelName': self.model_name, 'modelPluralName': 'people', 'properties': properties}
        exit(details)
        src.substitute(details)

    def get_input_names(self, transformer_array):
        return list(map(self.make_property, transformer_array))

    @staticmethod
    def make_property(name):
        " *     @SWG\Property(property = " + name.split("=>")[0]+ ", type = 'string', default = ''),"