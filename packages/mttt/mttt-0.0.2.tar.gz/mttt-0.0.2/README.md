# mttt

Minimalistic timetracking tool



### install

`pip install mttt`



## commands:

* start

initiate a project / task

* add

create a new task in a project
  If no project name is given, it will use the latest (current) project

example:

`t.py add myproject:"My latest task" `

example:

`t.py add secondtask `



* end

end a Task

example:

`t.py end finished`

* projects

list all projects

* report

Display the project data  

* current

Show current project

* edit

Edit the project data in a text editor

### plain text

Data is stored in simple (per project) text-files in `~/ttprojects` folder  
