from APIDoccer.Swagger import Swagger

if __name__ == "__main__":
    path = "/Users/JoeWood/dev/api-laravel-mobileapi/app/Transformers/newPersonTransformer.php"

    model_name = "Person"
    swagger = Swagger(path, model_name).create_swagger_definition()
