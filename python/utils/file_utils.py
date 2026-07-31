import hashlib


def calculate_file_hash(file_path):
    """
    Calculate SHA256 hash of a file.
    """

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()