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
    option_list = sys.argv[2:]
    print('option_list = ', option_list)
    short_options = "p:"
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
        print('options = ', options)
        print()
        for option, argument in options:
            if option == '-p':
                sha1_hex = argument
        folder, filename = sha1_hex[:2], sha1_hex[2:]
        try:
            with open(f".git/objects/{folder}/{filename}", "rb") as file:
                byte_array = bytearray()
                chunk_size = 4096  # 4 Kb
                while True:
                    chunk = file.read(chunk_size)
                    if chunk == b"":
                        # end of file
                        break
                    byte_array.extend(chunk)
                print("byte_array = ", byte_array)
                decompressed_data = zlib.decompress(byte_array)
                return decompressed_data.decode('utf-8')

        except IOError:
            raise ValueError(f"Invalid blob {folder}{filename}")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
