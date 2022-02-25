# Additional Testing
I will be going through the project app by app stating what validation mechanisms there are in place, and what additional testing I have done to ensure the website is robust.

## The Checkout App
### If a user is not logged in, they should be rerouted back to the bag view and asked to log in
- This is indeed the case, the user is returned to the bag view and notified the specific reason via the message system. No Stripe charges occur.
### If a user is logged in but not subscribed, they should be sent to the checkout view to fill in card details
- This is indeed the case, The user is presented with their current details and can then fill in their card details. Stripe charges the subscription amount.
### If a user fails to checkout and isn't subscribed, they should not be subscribed
- The Stripe payment declining prevents this from occuring
### If a user is subscribed and proceeds to checkout, they should be sent to the checkout success view
- This is the case, the user bypasses the stripe input and is shown their successful order
### Other inbuilt validation
- The code itself contains checks to make sure a user is logged in to checkout.
- The code checks the user's profile information to ensure it exists. If not then it is picked up by the order form check. This results in the user being returned to the checkout view.
- The code has a try except to ensure that an invalid product retrieval doesn't result in a crash

## The Bag App
### If the user adds a product to their bag, the product should get added and the user should be notified
- The product does indeed get added successfully, the message system lets the user know that the pokemon has been added, and the product count in the nav bar increments to show this.
### If the user adds a product to their bag, the product shouldnt be able to be added again
- There is protection in the code ensuring that the add to bag method is only run if the item isn't contained in the bag already. The product's detail page also has the add button removed and replaced with browse/checkout options instead. 
### If the user removes a product from their bag, the product should get removed and the user should be notified
- The product does indeed get removed successfully, the message system lets the user know that the pokemon has been removed, and the product count in the nav bar decreases to show this.
### When viewing their bag, if the bag is empty the user should be notified
- The bag does this by having a check to see if the bag is empty, if so then the bag view changes to notify the user as well as adding a button to let them browse. It removes the submit button.
### When viewing their bag, if the bag has content, it should all be displayed for the user
- The bag does this in a table-like format to show the user all the pokemon that have been added, and their specific details

## The Profile App and Allauth
### A user who is not signed in, should not have access to the profile app
- This is the case, the link is not visible to those not logged in, there is also extra validation in the view to return the user if they are not authenticated.
### A user who is signed in shouldn't have access to the login/signup pages
- The links are removed from the nav if the user is logged in.
### A user should be able to see their details
- The details for the user used in checkout are displayed on the left, including the subscription status.
### A user should be able to change their details
- The user can update their details, this is saved to their profile. They cannot edit their subscription status.
### A user should be able to see their past orders
- The previous orders of the user are displayed for them
### A user registering to the website shouldn't be able to enter incomplete data
- Allauth is able to verify emails are correct, as well as ensure no fields are left empty. The data itself gets double checked as the user has to enter their email and password twice
### A user should be sent a verification email allowing them to verify on the website
- This works allowing users to sign up to the website

## The Goods App
### All pokemon should display if no category is selected, and should have a way to handle displaying that much data
- This works, and there is a page system implemented into the goods app which calculates how many pages are needed based on the number of pokemon entries. This breaks up the website and makes it load much faster.
### All pokemon of a specific type should display if a type is clicked in the navbar dropdown
- This works, searching both the first and second type to ensure all possible pokemon under the criteria get added
### All pokemon containing the posted text string should display if a user inputs text via the navbar searchbar
- This works and helps narrow things down a lot
### If a pokemon only has one type, it should only display one
- As pokemon can be 1 or 2 types, I created a 19th empty type to handle this ensuring each pokemon has its types displayed correctly
### If a pokemon image is clicked it should take the user to a more detailed view
- This is the case
### Non-superusers should not be able to access any product add/edit/delete methods
- Links to the CRUD methods only exist for superusers. The methods themselves have checks to ensure the user is a superuser only else they get returned.