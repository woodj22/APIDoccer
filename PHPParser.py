

class PHPParser:
    def __init__(self, traversed_files):
        for files in traversed_files:
            for models in traversed_files[files]:
                with open(files+"/"+models) as f:
                    lines = f.readlines()
                content = [x.strip() for x in lines]
                content = filter(None, content)
                print content
                for lines in content:
                    print lines











