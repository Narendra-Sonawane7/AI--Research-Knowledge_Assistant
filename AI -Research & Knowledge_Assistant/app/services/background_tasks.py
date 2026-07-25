from fastapi import BackgroundTasks


def process_document(
        file_path
):

    print(
        f"Processing {file_path}"
    )