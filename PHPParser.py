

class PHPParser:
    def __init__(self, traversed_files):
        for files in traversed_files:
            for models in traversed_files[files]:
                with open(files+"/"+models) as f:
                    lines = f.readlines()
                content = [x.strip() for x in lines]
                content = filter(None, content)
                self.findProtectedFields(content)

    def findProtectedFields(self, content):
        def findProtection(string):
            return "protected" in string
        filteredContent = filter(findProtection, content)
        print filteredContent








