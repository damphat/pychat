import sys
from . import cli
from . import web

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        web.main()
    else:
        cli.main()

if __name__ == "__main__":
    main()
