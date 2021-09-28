# SA Exercise
## Important variables
* `FILE_TO_READ`
    * Sets the input file to be read
* `SOLUTION_FILE`
    * Sets the output file and directory for the parsed solution

## Run the program
This project uses python 3.9.6. To install all required dependencies run:

`pip3 -r requirements.txt`

To run the algorithm (takes a very long time for the large dataset):

`python main.py`

## Future work
### Initial state
Sort the tasks by difficulity and distribute them evenly on all the cores. The faster cores get the more time consuming tasks while slower cores get shorter tasks.
