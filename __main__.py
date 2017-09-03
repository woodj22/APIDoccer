from apidoccer.swagger import Swagger

if __name__ == "__main__":
    transformer_path = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Transformers/newPersonTransformer.php"
    #path = "/Users/BBCWood/dev/api-laravel-mobileapi/app/Transformers/PersonTransFormer.php"

    attributes = {
        'model_name': "Person",
        'plural_model_name': "People",
        'path': 'asf'
                  }
    swagger = Swagger(**attributes).create_swagger_definition(transformer_path)
   # swagger = Swagger(**attributes).create_index_function('people')
    print(swagger)
