# santex-automation

Welcome to the GUI Test Automation Challenge!
This challenge is designed to evaluate your knowledge, skills, and problem-solving abilities in
GUI automation. We’re excited to see your technical skills, creativity, and problem-solving
abilities come to life through this exercise.

**What to Expect**

Identify and interact with web page elements.
Perform actions such as entering text, submitting forms, and validating results.
Simulate real-world QA scenarios through automation.

**Key Details**


Timeline: You have 1 week from the date you receive this challenge to complete it.
Live demo: During the interview, you’ll be required to run your solution live and explain
your code and approach.
Submission: Provide code in a GitHub repository along with instructions README.md
for setup and execution.
Framework: You may use any of the following frameworks (C# and Python are
preferred):

- Playwright
- Selenium

Gen AI usage: We encourage the use tools like GitHub Copilot, ChatGPT, Claude, etc.,
to support your development. However, be prepared to demo and explain your solution
in detail during the interview.

By the end of this challenge, you should demonstrate proficiency in creating reliable and
maintainable automation test scripts, effectively analyzing and debugging issues during live
execution, and showcasing problem-solving skills to handle edge cases and dynamic content.
Good luck, and we look forward to reviewing your submission!

**UI Automation Challenge**
Welcome to the UI automation challenge! In this task, you’ll develop a solution to validate
various UI automation scenarios using the SauceDemo Shop web application.

**Tasks to Include for Each Use Case**

-Ensure your code follows a clean directory structure (e.g., separate test files, utility files,
and configurations).

-Avoid fragile locators like absolute xpaths. Focus on more robust strategies (e.g., data
attributes, ids).

-Validate results for every action (e.g., success/error messages).

-Include chained actions where relevant, simulating real-world flows.

-Use Appropriate Wait Strategies.

-Build reusable methods for commonly repeated actions.

-Store locators in a central location or class (e.g., using Page Object Model) to make your
code scalable and maintainable.

- Separate setup, action, and validation logic in your test scripts to maintain readability
and modularity.

**Optional Tasks to Showcase Your Skills**

- Use randomized or parameterized test data.
- Simulate cross-browser and multi-resolution scenarios.
- Implement retry logic for flaky tests.
- Generate detailed test execution reports (e.g., Allure report, HTML report).

**Use Cases to Automate**

| ID     | Title                              | Precondition                                                         | Steps                                                                                                                                                                                                                           | Expected Result                                                                                                             |
|--------|------------------------------------|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| TC 1.1 | Valid login                        | - Valid credentials (standard user/secret_sauce).                                                                   | 1. Navigate to https://www.saucedemo.com/ <br>2. Enter a valid username and password <br>3. Click "Login"                                                                                                                       | User successfully logs in and lands on the products page.                                                                    |
| TC 1.2 | Invalid login                      | –                                                                    | 1. Enter an invalid username or password <br>2. Click "Login"                                                                                                                                                                   | An error message is displayed.                                                                                                |
| TC 2.1 | Add a single product to the cart   | User is logged in.                                                   | 1. Click "Add to cart" for a single product                                                                                                                                                                                     | The cart badge updates to show (1).                                                                                           |
| TC 2.2 | Add multiple products to the cart  | User is logged in.                                                   | 1. Add multiple products to the cart                                                                                                                                                                                            | The cart badge reflects the correct number of items added.                                                                    |
| TC 3.1 | Remove product from cart           | User is logged in. <br> User has at least one product in the cart.   | 1. Go to the cart page <br>2. Click "Remove" for a product                                                                                                                                                                      | The product is removed from the cart, and the cart badge updates correctly.                                                   |
| TC 4.1 | Successful checkout                | User is logged in. <br> User has at least three products in the cart.| 1. Navigate to the cart page and click "Checkout" <br>2. Enter required details <br>3. Go to the checkout summary page <br>4. Validate total price matches sum of items + tax <br>5. Finish order                                | The order is placed successfully, and a confirmation message is displayed.                                                    |
| TC 4.2 | Checkout with Missing Details      | User is logged in. <br> User is on the checkout form.                | 1. Leave one or more required fields empty <br>2. Attempt to proceed                                                                                                                                                            | A field validation error is displayed.                                                                                        |
| TC 5.1 | Sort Products by Price (Low-High)  | User is logged in.                                                   | 1. On the Products page, select "Price (low to high)" from the dropdown                                                                                                                                                         | Products are displayed in ascending order of price, with the cheapest item first.                                             |
| TC 6.1 | Logout                             | User is logged in.                                                   | 1. Click the burger menu icon <br>2. Click "Logout"                                                                                                                                                                             | User is redirected to the login page and successfully logged out.                                                             |

