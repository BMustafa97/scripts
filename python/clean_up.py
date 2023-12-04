import os

# Get the current working directory
cwd = os.getcwd()
print("\033[34m" + f"Current working directory: {cwd}" + "\033[0m")

# Loop through all the files in the current directory
for filename in os.listdir(cwd):
    # Get the extension of the file
    extension = os.path.splitext(filename)[1]
    # Create a directory with the name of the extension if it doesn't already exist
    if extension and extension not in ['.py', '.sh']:
        directory = os.path.join(cwd, extension[1:])
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("\033[34m" + f"Created directory: {directory}" + "\033[0m")
        # Move the file to the directory with the same extension
        os.rename(os.path.join(cwd, filename), os.path.join(directory, filename))
        print("\033[32m" + f"Moved file {filename} to directory {directory}" + "\033[0m")
