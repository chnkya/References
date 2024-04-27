

**Requirements
*Python Interpreter:
    Python 3.7.4 or later
*Python Modules:
    requests-2.22.0
    validators-0.14.0

**Assumptions
1. Assumed the webservice is running on default port 80.
2. Has Set the logging level to ERROR to make the output clean. Please set to INFO for more detailed output.

**How to run this program ?
1. All requirements has to be installed on the server prior to running the program.
2. Make sure to use Python 3.7.4 or later.
3. Install Modules with pip (Version 19.2.2 or later). Modules can be installed using pip utility.
    pip install 'requests==2.22.0'
    pip install 'validators-0.14.0'
4. Once the modules are installed, Please copy the python script to a folder with servers.txt file.
5. Please make sure the permissions on the file to be executable and The running user has to the rights to write a file in the same folder.
6. Run the script with command "python coding_challenge.py".
7. The file will emit output to command prompt and will create a file "results.txt" in JSON format.

**Future Work:
1. Ordered Dictionaries for Results.
2. Restrict number of Threads to CPU threads by Default and ability to pass number of threads at the run time as parameter for parallelism.eiddccidrihbucdfjdifneeehcbgknnijllgidtjgfkg



