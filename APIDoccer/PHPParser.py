

class PHPParser:

    def __init__(self, traversed_files):
        global content
        content = self.getContentFromFiles(traversed_files)
    def getContentFromFiles(self, traversed_files):
        for files in traversed_files:
            for models in traversed_files[files]:
                with open(files+"/"+models) as f:
                    lines = f.readlines()
                ##strip white space out
                content = [x.strip() for x in lines]
                content = list(filter(None, content))

                return content

    def findProtectedFields(self):
        return filter(lambda string: "protected" in string, content)








