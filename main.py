from .ingest import *

INPUT_DIRECTORY = os.path.join(compute_file_directory(__file__), 'Key Bindings')
def set_up():
    create_directory_if_nonexistent(INPUT_DIRECTORY)
    context_set = ContextSet()
    context_set.load(INPUT_DIRECTORY)
    
set_up()
