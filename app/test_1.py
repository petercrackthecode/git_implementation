"""
+ What happens when you run the command git hash-object -w <file_name>
- Read the file with the provided path <file_name> as bytearray.
- Compress the bytearray using zlib (utf-8 encoding).
- Using hashlib's SHA-1: add the compressed data to the hashing variable, then return the hexdigest()
- Get the first two characters of the hashed hex as the subfolder, and the remaining 38 characters as the file (there 
are 40 characters in total).
- Save the compressed data as bytes to f".git/objects/{subfolder}/{file}"
"""
import zlib
import hashlib
import os


def hash_object(file_name):
    try:
        bytes = bytearray()
        with open(file_name, "rb") as file:
            byte = file.read(1)
            while byte:
                bytes += byte
                byte = file.read(1)
            file_content_string = bytes.decode(encoding='utf-8')
            header = bytearray(
                f'blob #{len(file_content_string)}\0', encoding='utf-8')
            print('header = ', header)
            compressed_data = zlib.compress(header + bytes)
            sha1 = hashlib.sha1()
            sha1.update(compressed_data)
            compressed_data_sha1 = sha1.hexdigest()
            subfolder, compressed_file_name = compressed_data_sha1[:2], compressed_data_sha1[2:]
            folder_path = os.path.join(".peter_git", "objects", subfolder)
            # Create folder
            os.mkdir(folder_path)
            # Create a file (in case it doesn't exist) and write the blob to it
            with open(os.path.join(folder_path, compressed_file_name), 'wb') as compressed_file:
                compressed_file.write(compressed_data)
    except IOError:
        raise ValueError(f"Unable to open file {file_name}: File not found")


# with open('.peter_git/objects/8d/50dfb84b1cf69475c93c26e7ef5420bcb17810', 'rb') as file:
#     bytes = bytearray()
#     byte = file.read(1)
#     while byte:
#         bytes += byte
#         byte = file.read(1)
#     print("bytes after being decompressed: ",
#           zlib.decompress(bytes))

hash_object('example.txt')
