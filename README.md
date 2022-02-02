# Moxom
[![PyPI version](https://badge.fury.io/py/moxom.svg)](https://badge.fury.io/py/moxom)

Python library to build simple user-friendly CLI API for your Python scripts.  
Allows mapping commands to classes, class methods and functions.  
Supports both `def` and `async def`.  

Let's assume we have script `dumb_ci` with next class:
```python
from asyncio import sleep

class Computer:
    def __init__(self, computer_name: str = "Default"):
        self.computer_name = computer_name

    async def compile_code(self, project_name: str = "TestProject"):
        await sleep(2) # build something
        print(f"Built finished for {self.computer_name} {project_name}")
```
And next function:
```python
from asyncio import sleep

async def deploy_code(project_name: str = "TestProject"):
     await sleep(1)
     print(f"Deployed {project_name}")
```

With this library you are able to create simple API for CLI.
```shell script
./dumb_ci computer compile_code
```

Library allows passing parameters.
```shell script
./dumb_ci computer '"Build server #2"' compile_code '"MegaProject"'
```

You can order commands using basic shell tools
```shell script
./dumb_ci computer compile_code && ./dumb_ci deploy_code
./dumb_ci computer compile_code '"Project1"' & ./dumb_ci computer compile_code '"Project2"'
```

Additionally, you can use operators `and` (asynchronous), `then` (synchronous) and parentheses.
```shell script
./dumb_ci computer compile_code then deploy_code
./dumb_ci (computer compile_code then deploy_code) and (computer '"2"' compile_code '"Project2"' then deploy_code '"Project2"')
```

To list all available commands there is a `help` operator. 
```python
./dumb_ci help
> computer
> computer compile_code
> deploy_code
```

To obtain help for a specific command just add `help` before command.
If no help text provided in command definition, the one received with Python `help` command will be used.
```python
./dumb_ci deploy_code
> Deploys code
./dumb_ci computer compile_code
> Compiles code
```

## Integration

Assuming we have class `Computer` and function `deploy_code` from example above entire integration would look like this: 
```python
import sys
from moxom import Moxom, Routine, create_routines

routines = create_routines(            # Utility function to create Dict[str, Routine]
    Routine(                           # Class representation of a command in CLI
        "deploy_code",                 # Command name
        deploy_code,                   # Function to call
        help="Deploys code to AWS"     # Text for help
    ),
    Routine(                           # Class representation of a command in CLI
        "computer",                    # Command name
        Computer,                      # Constructor of class Computer and it is a function 
        subroutines=create_routines(   # As we want to invoke methods of Computer, we can specify subroutines 
            Routine(                   # which are represented by Computer class methods
                "compile_code",        # Subroutine name. "computer compile_code"
                Computer.compile_code, # Method of Computer to be called,
                help="Compiles code"   # which will receive instance created by "computer" as `self`
            )                          
        )
    )
)

if __name__ == '__main__':
    moxom = Moxom(routines)
    arguments = sys.argv[1:]
    moxom.execute(" ".join(arguments))
```

To increase comfortability you may want to have simple interactive mode
```python
if __name__ == '__main__':
    moxom = Moxom(routines)

    arguments = sys.argv[1:]

    if len(arguments) == 0:
        # interactive mode
        print("Interactive mode")
        while True:
            moxom.execute(input("> "))
    else:
        # single line mode
        moxom.execute(" ".join(arguments))
```

## Example
Example of usage and integration is [here](example/__main__.py).

## Basic usage
To integrate library into existing Python project, just import as in next line:
```python
from moxom import Moxom, Routine, create_routines
```
### Moxom
`Moxom` - library entry-point.  
Expects to receive `Dict[str, Routine]` on construction.
Optionally you can pass environment file path.  
Call `execute(line)` to process a single line of input.  

### Routine
`Routine` - class representation of a single command.  
It must have a name and a function to call.  
Optionally you may set subroutines and `help` text.

### create_routines  
`create_routines` - Utility function to create `Dict[str, Routine]`.

## Operators
### And
Allows running commands asynchronously, `&` in Shell, maps to `asyncio.gather`.  
```
# Starts computers simultaneously
computer "1" start and computer "2" start
```

### Then
Allows running commands consequently, `&&` in Shell, maps to consequent code with `await`.  
```
# Starts computer 1, waits for it to start, and then starts computer 2
computer "1" start then computer "2" start
```  

### Parentheses
To specify higher precedence of operation, you can use parentheses.
```
# Start computer 1 and computer 2 simultaneously.
# Wait for both to start.
# Then shut down both computers 1 and 2 simultaneously.
(computer "1" start and computer "2" start) then (computer "1" shutdown and computer "2" shutdown)
```

### Help
To list all available commands there is a `help` operator. 
```python
./dumb_ci help
> computer
> computer compile_code
> deploy_code
```

To obtain help for a specific command just add `help` before command.
If no help text provided in routine definition, the one received with Python `help` command will be used.
```python
./dumb_ci deploy_code
> Deploys code
./dumb_ci computer compile_code
> Compiles code
```


## Declarations
Commands and variables can be declared with `=` operator.  
It can be a declaration of an argument.  
```
> mega_project = "MegaProject"

# returns "MegaProject"
> mega_project
```
Or of a function.  
```
> comp2_mega_full_ci = computer "Comp2" compile_code "MegaProject" then deploy_code "MegaProject"

# runs code
> comp2_mega_full_ci   
```
Additionally, you can provide arguments for a function.
```
> full_ci comp proj = computer comp compile_code proj then deploy_code proj

# runs full ci on Comp2 for MegaProject
> full_ci "Comp2" "MegaProject" 

# declares a function
> comp2_mega_full_ci = full_ci "Comp2" "MegaProject"

# runs full ci on Comp2 for MegaProject
> comp2_mega_full_ci
```


## Known issues
When strings are passed from shell to python, shell removes quotes.     
`./dumb_ci computer "Build server #2" compile_code` is parsed as `computer Build server #2 compile_code` and leads to exception.

Using from Shell you have to wrap strings twice with double quotation marks, or with quotes and escaping 
or by using both single quotes and double quotes:
```shell script
./dumb_ci computer '"Build server #2"' compile_code
``` 

## Environment
If you want to create simple scenarios with Moxom syntax or just to specify variables on script startup, 
you can create a file with commands, which will be executed on Moxom initialization.
```python
env_file = os.path.join(os.path.dirname(__file__), "example_mox_env.ini")
moxom = Moxom(routines, moxom_env=env_file)
```

You can find example of environment file in [example_mox_env.ini](example/example_mox_env.ini) 
and integration in [example module](example/__main__.py).
