import sys
import os
import getopt
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    argument_list = sys.argv[1:]
    print('argument_list = ', argument_list)
    short_options = "p:"
    try:
        arguments_options = getopt.getopt(argument_list, short_options)[1]
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
        print('arguments_options = ', arguments_options)
        for argument, value in arguments_options:
            if argument == '-p':
                sha1_hex = value
        folder, filename = sha1_hex[:2], sha1_hex[2:]
        try:
            with open(f".git/objects/{folder}/{filename}", "rb") as file:
                byte_array = bytearray()
                while (byte := file.read(1)):
                    byte_array += byte
                return byte_array.decode('utf-8')

        except IOError:
            raise ValueError(f"Invalid blob {folder}{filename}")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
