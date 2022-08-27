import sys
import os
import getopt
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    option_list = sys.argv[2:]
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
        for option, argument in options:
            if option == '-p':
                sha1_hex = argument
        folder, filename = sha1_hex[:2], sha1_hex[2:]
        ENCODE_TYPE = DECODE_TYPE = 'utf-8'
        try:
            with open(f".git/objects/{folder}/{filename}", "rb") as file:
                byte_array = bytearray()
                chunk_size = 4096  # 4 Kb
                byte = file.read(1)
                while byte:
                    byte_array.append(byte)
                    byte = f.read(1)
                decompressed_data = zlib.decompress(byte_array)
                print(decompressed_data.decode(DECODE_TYPE), end="")
                return decompressed_data.decode(DECODE_TYPE)

        except IOError:
            raise ValueError(f"Invalid blob {folder}{filename}")
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
