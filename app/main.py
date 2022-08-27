import sys
import os
import getopt
import zlib
import hashlib


def hash_object(file_name):
    try:
        bytes = bytearray()
        with open(file_name, "rb") as file:
            byte = file.read(1)
            while byte:
                bytes += byte
                byte = file.read(1)
            file_content_string = bytes.decode(encoding='utf-8')
            # This header is required by the blob object format: https://git-scm.com/book/en/v2/Git-Internals-Git-Objects
            header = bytearray(
                f'blob #{len(file_content_string)}\x00', encoding='utf-8')
            # Files data are converted to sha1 first before being compressed.
            sha1 = hashlib.sha1()
            sha1.update(bytes)
            data_sha1 = sha1.hexdigest()
            subfolder, compressed_file_name = data_sha1[:2], data_sha1[2:]
            folder_path = os.path.join(".git", "objects", subfolder)
            # Create folder
            os.mkdir(folder_path)
            compressed_data = zlib.compress(bytes)
            # Create a file (in case it doesn't exist) and write the blob to it
            with open(os.path.join(folder_path, compressed_file_name), 'ab') as compressed_file:
                compressed_file.write(header)
                compressed_file.write(compressed_data)
            # print the data_sha1 as the desired stdout of the function
            print(data_sha1, end="")
            print('\nfile_content_string = ', file_content_string, end="")
    except IOError:
        raise ValueError(f"Unable to open file {file_name}: File not found")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    option_list = sys.argv[2:]
    short_options = "p:w:"
    try:
        options, _ = getopt.getopt(option_list, short_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")
    elif command == "cat-file":
        for option, argument in options:
            if option == '-p':
                sha1_hex = argument
        folder, filename = sha1_hex[:2], sha1_hex[2:]
        DECODE_TYPE = 'utf-8'
        try:
            with open(f".git/objects/{folder}/{filename}", "rb") as file:
                byte_array = bytearray()
                byte = file.read(1)
                while byte:
                    byte_array += byte
                    byte = file.read(1)
                decompressed_data = zlib.decompress(byte_array)
                # filter out the "blob" and file length strings
                decompressed_data = decompressed_data[(
                    decompressed_data.find(b'\x00') + 1):]
                print(decompressed_data.decode(DECODE_TYPE), end="")

        except IOError:
            raise ValueError(f"Invalid blob {folder}{filename}")
    elif command == 'hash-object':
        for option, argument in options:
            if option == '-w':
                input_file_name = argument
        try:
            hash_object(input_file_name)
        except Exception as exc:
            raise RuntimeError(exc)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
