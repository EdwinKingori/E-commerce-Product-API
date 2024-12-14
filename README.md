E-commerce Product API
The E-commerce product api project will involve implementing CRUD (Create,Read, Update, Delete) operations to allow users to interact with the products data. The project will use various endpoints that will enable users to access a list of products, single product, and interact with the search functionality to search for specific products. 
Additional endpoints will include a pagination route that will restrict the product listing to be 10 products per page and nested routing that will simplify filtering capabilities such as searching products for a given user and searching for products under a certain category. 

Url Configuration for the CRUD, Search and Nested endpoint operations 
Products CRUD:
POST /api/products/
GET /api/products/
GET /api/products/{id}/
PUT /api/products/{id}/
DELETE /api/products/{id}/
Search & Filtering:
GET /api/products/?search=<name>
GET /api/products/?category=<category>
GET /api/products/?ordering=price
User Management:
POST /api/users/
GET /api/users/
Nested Product Collections:
GET /api/users/{user_id}/products/

