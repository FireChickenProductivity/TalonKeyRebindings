from .ingest import ContextSet
from .generator import TalonBuilder, TalonGenerator
from .fire_chicken.path_utilities import compute_file_directory, create_directory_if_nonexistent
import os

INPUT_DIRECTORY = os.path.join(compute_file_directory(__file__), 'Key Bindings')
OUTPUT_DIRECTORY = os.path.join(compute_file_directory(__file__), 'talon_output')
TAG_MANAGER_FILEPATH = os.path.join(compute_file_directory(__file__), 'tag_manager.py')
def set_up():
    create_directory_if_nonexistent(INPUT_DIRECTORY)
    create_directory_if_nonexistent(OUTPUT_DIRECTORY)
    context_set = ContextSet()
    builder = TalonBuilder(context_set)
    generator = TalonGenerator(builder, OUTPUT_DIRECTORY, TAG_MANAGER_FILEPATH)
    context_set.load(INPUT_DIRECTORY)

set_up()
