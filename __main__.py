from apidoccer.swagger import Swagger

if __name__ == "__main__":
    path = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Transformers/newPersonTransformer.php"
    #path = "/Users/BBCWood/dev/api-laravel-mobileapi/app/Transformers/PersonTransFormer.php"

    attributes = {
        'model_name': "Person",
        'plural_model_name': "People"
                  }
    swagger = Swagger(path, **attributes).create_swagger_definition()
    print(swagger)
