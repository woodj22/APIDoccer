

class PHPParser:

    def __init__(self, traversed_files):
        global content
        content = self.getContentFromFiles(traversed_files)
        print content
    def getContentFromFiles(self, traversed_files):
        for files in traversed_files:
            for models in traversed_files[files]:
                with open(files+"/"+models) as f:
                    lines = f.readlines()
                content = [x.strip() for x in lines]
                content = filter(None, content)

                return content

    def findProtectedFields(self):
        def findProtection(string):
            return "protected" in string
        return filter(findProtection, content)








