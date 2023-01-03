# CS50 Eats

## Video Demo:  https://www.youtube.com/watch?v=5v1ls7vkRSY&ab_channel=PatrikP%C3%A1tek 

## Description:
### Core:
CS50 Eats is my final project for CS50's Introduction to Computer Science course.
It is a food delivery app using flask in python (naturally combined with HTML and CSS).

first of all, you have to be registered through a custom form where you have to fill in at least the required fields.
- Username
- E-mail
- Password and password confirmation
The form asks for more pieces of information which frankly do not have any use at the moment.

Once you have finished your registration, you are welcomed to the main page of the app.
This route consists of all of the cards of partnered restaurants (more on that later).
You can choose your favorite and continue to the menu of that particular restaurant.

You can now select multiple products (unfortunately only one of each kind) and click confirm button to make a payment.
If you have enough balance in your bank account, you are good to go.

Registration -> order -> payment.

### Manage account:
At the top of the page, you can see the “manage account” button.
On this page, you can change your password or deposit money into your account.

### User status:
The highlight of the app is user status, which determines what you can do inside the app.
There are three different statuses:
-	Admin
-	Owner
-	User

Once you make your account, you are simply just a user, which means that you just use the app as stated before (order food).

From the user you can also become an owner of the restaurant, meaning that you can apply for a partnership and display your business on the home page of the app.
This can be done via a “become partner form”. There you need to fill in the restaurant name and optionally the description of it. Once you hit the “apply” button, you have to wait for approval from the admin.

Admin can see all of the awaiting requests and can either accept or decline the request.

If the admin decides to accept your request, you officially become a partner of CS50 Eats and can now manage your restaurant. You can add or remove the products including their prices of them.

## Error check:
There are no errors that occurred from the testing made. All works as intended.

## Possible improvements:
-	Add more options for the manage account section (name change, email change,…).
-	Ability to order more amount of the same product.
-	Ability to order from more restaurants at the same time.
-	Better handling of a preview picture of the restaurant (done manually at this point).
-	Add a footer to the lauout.html.