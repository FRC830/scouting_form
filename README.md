The 830 Scouting Form Base
==========================
###Purpose
This repository makes the creation of FRC scouting forms easier.
Using this as a submodule handles common form items and python flask servers that are reused each year.

###Using This Repository
Creating a custom scouting form is simple  
1. Create a new repository  
2. Add this submodule to your repository  
    `git submodule add https://github.com/FRC830/scouting_form.git`   
3. Copy the contents of the "example" folder from the submodule into your repository  
	Your repository should now contain 5 things: scouting_form, web, .gitignore, .gitmodules, and run.py  
4. Modify the code in the "web" folder to customize your form
