# django ecommerce
Django ecommerce website for education and practice reason

Website have trivial design. Frontend pages generated using free sources of bootstrap ( getbootsrap.com, startbootsrap , fontawesome version 4, and other ... ) javascripts not used on the code. Website have Basic functions of a ecommerce webshop: User registration with email confirmation ( currently work with locahost and fake mail server for testing ). User login, Password reset with email confirmation, Admin panel with possibility to add, remove, products and categories , manage orders. List categories, and products, search for price and name or description. Pagination implemented ( most of the cases ). Shopping cart both anonymous (sessions) and logged in user functions ( add, or remove items ). Create orders ( online payment method still not implemented). Send reviews to produts and star rating system etc ..

Website might have bugs what I'm not detected, or simple forget to fix. The code maybe seems to caotic, or possible over or under thinked. Possible missing some features ( this is my first project for practise and learn django .. so at least I tried it)

setup on linux:

#1. clone the repository

#2. cd ecommerce 

#3. set up new virtual environment ( virualenv venv )

#4. install requirements pip3 install -r requirements.txt

#5. make the initial migrations   manage.py makemigrations & manage.py migrate

#6. create admin user :  manage.py createsuperuser

#7. start use the app with manage.py runserver on localhost port : 8000 
