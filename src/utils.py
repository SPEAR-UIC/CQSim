import builtins
import contextlib
import random
import shutil
import os

def probabilistic_true(y):
  """
  Returns True with a probability of y.

  Args:
      y: A float between 0 and 1 representing the desired probability of returning True.

  Returns:
      True with a probability of y, otherwise False.
  """

  # Generate a random float between 0 and 1
  random_number = random.random()

  # Compare the random number to the input probability
  if random_number < y:
    return True
  else:
    return False

def get_elements_in_range(data_list, index, range):
  """
  Retrieves elements from a list within a specified range around a given index.

  Args:
      data_list: The list to extract elements from.
      index: The index around which to define the range.

  Returns:
      A list of elements within the range (index - 5, index + 5), 
      or an empty list if the range is invalid.
  """

  start = max(0, index - range)  # Ensure the start index is within bounds
  end = min(len(data_list), index + range + 1)  # Ensure the end index is within bounds

  if start >= end:  # Handle cases where the range is empty
      return []

  return data_list[start:end]

@contextlib.contextmanager
def disable_print():
  """Temporarily disables the print function."""
  original_print = builtins.print

  def disabled_print(*args, **kwargs):
    pass  # Do nothing when print is called

  builtins.print = disabled_print
  try:
    yield
  finally:
    builtins.print = original_print

@contextlib.contextmanager
def enable_print():
  """Context manager that ensures printing is enabled, even if previously disabled."""
  original_print = builtins.print
  builtins.print = original_print  # Restore original print if needed
  try:
    yield
  finally:
    pass  # No need to do anything in the finally block

def delete_file(file_path):
  """
  Deletes a file.

  Args:
    file_path: The path to the file to be deleted.
  """
  try:
    os.remove(file_path)  # You can also use os.unlink(file_path)
  except FileNotFoundError:
    print(f"File not found: {file_path}")
  except PermissionError:
    print(f"Permission denied to delete {file_path}")
  except Exception as e:
    print(f"An error occurred: {e}")
