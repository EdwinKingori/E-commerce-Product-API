E-commerce Product API

The E-commerce product api project will involve implementing CRUD (Create,Read, Update, Delete) operations to allow users to interact with the products data. The project will use various endpoints that will enable users to access a list of products, single product, and interact with the search functionality to search for specific products. 
Additional endpoints will include a pagination route that will restrict the product listing to be 10 products per page and nested routing that will simplify filtering capabilities such as searching products for a given user and searching for products under a certain category. 

Url Configuration for the CRUD, Search and Nested endpoint operations 

Products CRUD:

	POST /shopify/products/
	GET /shopify/products/
	GET /shopify/products/{id}/
	PUT /shopify/products/{id}/
	DELETE /shopify/products/{id}/

Orders CRUD:

	POST/shopify/orders/
	GET/shopify/customers/
	GET/shopify/customers/{id}/

Customers:

	POST/shopify/customers/
	GET/shopify/customers/
	GET/shopify/customers/{id} 

Cart

	POST/shopify/carts/
	GET/shopify/carts/items/

Search & Filtering:

	GET /shopify/products/?search=<name>
	GET /shopify/products/?category=<category>
	GET /shopify/products/?ordering=price

User Management:

	POST /shopify/users/
	GET /shopify/users/
	Nested Product Collections:
	GET /shopify/users/{user_id}/products/


 Authentication Endpoints

   Obtain Token: Obtain a JWT token for authentication.
	
	 http://127.0.0.1:8000/auth/jwt/create
	Method: POST
 
   Login Url: To obtain the token user
   
   	 http://127.0.0.1:8000/auth/users/me/
	 Method: GET
	


Setup to Fork or Clone:

Fork the Repository

	Click on the Fork button in the top-right corner.
	
	Clone the Repository

Copy the repository URL from your fork.

	Run the following command in your terminal:
	
	git clone <repository-url>

Set Up the Environment

Navigate to the project directory:
	
	cd ecommerce_api

Create and activate a virtual environment:

	python3 -m venv venv
	source env/bin/activate  # For Linux/Mac
	env\Scripts\activate   # For Windows

Install dependencies:

	pip install -r requirements.txt
	
Run the Project Locally

	
Apply migrations:
	
	python manage.py migrate

Start the development server:

	python manage.py runserver
	
Visit: to interact with the API

	http://127.0.0.1:8000/shopify/ 
