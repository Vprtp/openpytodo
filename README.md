# OpenPyToDo

A simple and lightweight to-do program based on Pyhon. It allows you to store and view tasks of different importance, separated in various "projects".

## Installation

The program requires Python 3.12 to be installed on the machine to run. No further setup is required because all the libraries it uses should be contained within a standard Python installation.\
Simply download the repository to begin using the program. To start it, run `python main.pyw` (`python3 main.pyw` on Linux-based systems).\
It's reccomended to create a link/shortcut to the program to facilitate regular use.

## Data

All data of the program is saved inside of the `./data` directory. Each project has a separate file.

## Usage

The program interface is separated in two main sections: the top section and the bottom section.\
\
The *top section* allows you to view the tasks in the loaded project in order of importance and of their creation date.\
It's a list with three columns: each line corresponds to a task; the first column shows its importance, the second column its description, and the third shows its creation date.\
If a task description is too long to be viewed in the list, you can double click on it to view it in a separate window.\
\
The *bottom section* contains all the action interfaces.
- There is a text box with a drop-down menu: there you can write the description and select the importance of the next task you'd like to add.
- The `Add Task` button allows you to add a task to the project with the description and importance given in the previously described interface.
- The `Delete Task` button deletes the selected task.
- The `Edit Task` button opens a window which allows you to modify the description and the importance of the selected task.
- The `Load Project` button allows you to open a project file within the ones in the data directory.
- The `New Project` button allows you to create a new project with a given name. This will create a new project file in the data directory.
- The `Edit Project` button opens a window which allows you to edit the loaded project's name.
- The `Save Project` button saves all the changes to the currently loaded program.
- The `Delete Project` button deletes the project file to the currently loaded project. It's a permanent operation, so it requires confirmation. Deleting a project will also permanently delete its tasks, so do it carefully.
- The `Quit` button closes the program. If there are any unsaved changes, it will ask for confirmation.

By _Vprtp_ (on GitHub, _prtp_ elsewhere)
