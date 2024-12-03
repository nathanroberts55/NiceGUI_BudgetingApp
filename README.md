## Setup for Development

1. Comment out the second `ui.run()` in the `main.py` file and uncomment out the second one labeled "For Development"
2. Update the `config.py`
   1. Change `DEBUG` to `TRUE`
3. In a terminal within the project folder, run `python main.py`

## Building the App for "Production" Use
Instructions are based off video here: [Convert GUI App to Real Program - Python to exe to setup wizard](https://youtu.be/p3tSLatmGvU?si=M94vlGYcaUSZAibx)

1. Comment out the second `ui.run()` in the `main.py` file
2. Update the `config.py`
   1. Change `DEBUG` to `FALSE`
   2. Update the version number
3. Run the `build.py` script
4. Update the `BudgetingAppSetupScript.iss` file
   1. Needs new GUID for the `AppId`
   2. Update the `MyAppVersion` and `OutputBaseFilename`
5. Run the Inno Setup Program using the `BudgetingAppSetupScript.iss` file
6. Install in the `Documents/BudgetingApp/` directory (has to be a location with write permissions for this kind of app)