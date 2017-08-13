

class Swagger:
    def __init__(self, path):
        self.transformerFilePath = path

        with open(self.transformerFilePath) as f:
            lines = f.readlines()
        content = [x.strip() for x in lines]
        found_start = False

        for index, line in enumerate(content):
            if "public $map" in line:
                start_point = index + 1
                found_start = True
            if found_start and "];" in line:
                end_point = index

        i = self.get_input_names(content[start_point:end_point])
        print(i[0])

    def get_input_names(self, mapped_array):
        return [name.split("=>") for name in mapped_array]
