import os
import datetime

def create_diary():
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")
    diary_dir = "diary_notes"
    if not os.path.exists(diary_dir):
        print(f"Creating directory: {diary_dir}")
        os.mkdir(diary_dir)
    strdate = datetime.datetime.today().strftime('%Y-%m-%d_%H%M%S')
    file_name_for_today = f"note_{strdate}.md"
    print(f"Today's file name would be: {file_name_for_today}")
    target_path_for_diary = os.path.join(diary_dir, file_name_for_today)
    title = f"""# {strdate}

This is a temporary note for my daily learning.
Contents will be moved to other places later.
    """
    if os.path.exists(target_path_for_diary):
        print(f"File {target_path_for_diary} already exists.")
    else:
        try:
            create_file(target_path_for_diary, title)
        except ValueError as e:
            print(f"Error: {e}")


def create_file(fname: str = None, title: str = "# Diary Entry\n"):
    """Create a file with the given name and initial content.
    Args:
        fname(str): The name of the file to create. This argument is required.
        title(str): The initial content to write to the file. Defaults to "# Diary Entry\n" for markdown files.

    Raises:
        ValueError: If fname is None.
    """
    if fname is None:
        raise ValueError("Filename must be provided.")
    with open(fname, "a") as f:
        f.write(title)

if __name__ == "__main__":
    create_diary()