import zlib
import binascii
import hashlib

data = 'Hello world'

compressed_data = zlib.compress(bytes(data, 'utf-8'))
m = hashlib.sha1()
m.update(compressed_data)
compressed_data_sha1 = m.hexdigest()

print("Original data: " + str(data))
# print("Compressed data: " + str(compressed_data))
# print("Compressed data in SHA-1: ", compressed_data_sha1)
# print("len(compressed_data_sha1) = ", len(compressed_data_sha1))
print("Binary data after being decompressed: ",
      zlib.decompress(compressed_data))
print(
    f"Original data after being decompressed: '{zlib.decompress(compressed_data).decode('utf-8')}'")

"""
+ What happens when you run the command `git cat-file -p <sha1-hex>`?
- Get the first two characters of the sha1-hex hash as the subdirectory.
- Get the following 38 characters of the sha1-hex has as the filename.
- Read the file content as bytes.
- Decompress the file content using zlib (return a bytes string)
- Convert the bytestring to a string.
- Return the string as the result of the cat-file command.
"""
