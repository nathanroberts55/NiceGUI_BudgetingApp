# Budget Tracking App

## Problem Statement

I currently track my budget using a multi-page excel sheet. These sheets are broken down by month and give a general overview of my finances during that month long period. However, since each sheet stands alone with no relation to other sheets, if I wanted a wider/narrower scope I would have to create new sheets and the cell logic would be exponentially more sophisticated. Meaning that I have no view that can display my budget over any other time frame. I also must manually filter and sort the data. Additionally, the data is all stored as text, and I have no visual representation of the information for gaining insights briefly. Lastly, I have had many people ask for the excel sheet to track their own budget, however, in its current state it is only really digestible to me and requires a lot of onboarding for new users.

## Proposed Solution

My proposed solution is using a desktop app that can be created, adapted, shared, and downloaded that will allow for me and other users a more friendly experience that incorporates the current functionality of the existing solution as well as lower the level of effort required to expand to meet the new requirements.

This desktop application will allow users to enter in their planned budget details, then track their actual income, expenses, savings, etc that incorporate their planned budget. This application will have a more friendly user interface that will allow for users of various technical expertise to use and share the application. The application will store user data in a database local to their machine to persist the saved information. The information stored in the database will be used to present tabular as well as graphical representations of the users information in a financial dashboard. Finally, the application will be able to export the data from a given timeframe into a file format that the user can use and share with others.

### Solution Reach Goals

Below are some goals of the solution that would be great to accomplish but may be out of scope:

- Ability to customize the financial dashboard screen.
- Export to Budget data to Excel format for users that are more comfortable using excel.
- Import data from excel template. This way users that were using the old excel solution can import their past data. As well as formats that would allow for mass data imports.

## Requirements

### Functional Requirements

#### Stakeholder Identification & Classification

- Application Users
- External Users

#### User Stories

- As a User, I want to create an estimate line item/transaction for my Income as part of my Planned Budget.
- As a User, I want to read an estimate line item/transaction for my Income as part of my Planned Budget.
- As a User, I want to delete an estimate line item/transaction for my Income as part of my Planned Budget.
- As a User, I want to update an estimate line item/transaction for my Income as part of my Planned Budget.
- As a User, I want to create an estimate line item/transaction for my Expenses as part of my Planned Budget.
- As a User, I want to read an estimate line item/transaction for my Expenses as part of my Planned Budget.
- As a User, I want to update an estimate line item/transaction for my Expenses as part of my Planned Budget.
- As a User, I want to delete an estimate line item/transaction for my Expenses as part of my Planned Budget.
- As a User, I want to create an estimate line item/transaction for my Spending as part of my Planned Budget.
- As a User, I want to read an estimate line item/transaction for my Spending as part of my Planned Budget.
- As a User, I want to update an estimate line item/transaction for my Spending as part of my Planned Budget.
- As a User, I want to delete an estimate line item/transaction for my Spending as part of my Planned Budget.
- As a User, I want to create an estimate line item/transaction for my Debt as part of my Planned Budget.
- As a User, I want to read an estimate line item/transaction for my Debt as part of my Planned Budget.
- As a User, I want to update an estimate line item/transaction for my Debt as part of my Planned Budget.
- As a User, I want to delete an estimate line item/transaction for my Debt as part of my Planned Budget.
- As a User, I want to create an estimate line item/transaction for my Savings as part of my Planned Budget.
- As a User, I want to read an estimate line item/transaction for my Savings as part of my Planned Budget.
- As a User, I want to update an estimate line item/transaction for my Savings as part of my Planned Budget.
- As a User, I want to delete an estimate line item/transaction for my Savings as part of my Planned Budget.
- As a User, I want to create a line item/transaction of my Income as part of my Actual Budget.
- As a User, I want to create a line item/transaction of my Expenses as part of my Actual Budget.
- As a User, I want to create a line item/transaction of my Spending as part of my Actual Budget.
- As a User, I want to create a line item/transaction of my Debt as part of my Actual Budget.
- As a User, I want to create a line item/transaction of my Savings as part of my Actual Budget.
- As a User, I want to see the Percent of Budgeted Money for each line item/transaction of the Budget.
- As a User, I want to see if I am over/under for each line item/transaction of the Budget.
- As a User I want to create a line item/transaction of the Beginning Balance of my Debts.
- As a User I want to read a line item/transaction of the Beginning Balance of my Debts.
- As a User I want to update a line item/transaction of the Beginning Balance of my Debts.
- As a User I want to delete a line item/transaction of the Beginning Balance of my Debts.
- As a User I want to create a line item/transaction of the Ending Balance of my Debts.
- As a User I want to read a line item/transaction of the Ending Balance of my Debts.
- As a User I want to update a line item/transaction of the Ending Balance of my Debts.
- As a User I want to delete a line item/transaction of the Ending Balance of my Debts.
- As a User I want to create a line item/transaction of the Interest Rates of my Debts.
- As a User I want to read a line item/transaction of the Interest Rates of my Debts.
- As a User I want to update a line item/transaction of the Interest Rates of my Debts.
- As a User I want to delete a line item/transaction of the Interest Rates of my Debts.
- As a User I want to create a line item/transaction of the Beginning Balance of my Savings.
- As a User I want to read a line item/transaction of the Beginning Balance of my Savings.
- As a User I want to update a line item/transaction of the Beginning Balance of my Savings.
- As a User I want to delete a line item/transaction of the Beginning Balance of my Savings.
- As a User I want to create a line item/transaction of the Ending Balance of my Savings.
- As a User I want to read a line item/transaction of the Ending Balance of my Savings.
- As a User I want to update a line item/transaction of the Ending Balance of my Savings.
- As a User I want to delete a line item/transaction of the Ending Balance of my Savings.
- As a User I want to create a line item/transaction of the Amount Spent of my Savings.
- As a User I want to read a line item/transaction of the Amount Spent of my Savings.
- As a User I want to update a line item/transaction of the Amount Spent of my Savings.
- As a User I want to delete a line item/transaction of the Amount Spent of my Savings.
- As a user, I want to see the Total Out Amount of my Budget.
- As a user, I want to see the Final Balance of my Budget
- As a user, I want to create inidividual transaction per budget group (Income, Spending, Debt, Savings).
- As a user, I want to read inidividual transaction per budget group (Income, Spending, Debt, Savings).
- As a user, I want to update inidividual transaction per budget group (Income, Spending, Debt, Savings).
- As a user, I want to delete inidividual transaction per budget group (Income, Spending, Debt, Savings).

### Technical Requirements

#### Entity Relationship Diagram

#### Technical Stack
