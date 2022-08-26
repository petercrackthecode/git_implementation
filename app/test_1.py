import getopt
import sys


def usage():
    print("\nThis is the usage function\n")
    print('Usage: '+sys.argv[0]+' -i <file1> [option]')


def main():
    print("Hi from test_1.py")
    try:
        opts, args = getopt.getopt(sys.argv[2:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    print('getopt initialized')
    output = None
    verbose = False
    print("opts = ", opts)
    for o, a in opts:
        if o == "-v":
            verbose = True
            print('verbose = True')
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print("output = ", output)
        else:
            assert False, "unhandled option"
    # ...


if __name__ == "__main__":
    main()
