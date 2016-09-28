usage: sweep [-h] [-r] [-b] [-f] [-l] [-s] [-d] [-e] [-v] [-m SECONDS]
               [-a SECONDS] -p PATH [-t REGEX]

collect outdated files and folders.

arguments:
  -h, --help            show this help message and exit
  -r, --recursive       do recursive search
  -b, --allow-root      allow process root path
  -f, --follow          follow symlinks
  -l, --allow-link      allow process symlinks
  -s, --allow-dir       allow process directories
  -d, --delete          delete each file instead of displaying its path
  -e, --collect-empty   collect empty directories
  -v, --verbose         echo each deleted file path to stdout
  -m SECONDS, --modified SECONDS
                        seconds from last modifying
  -a SECONDS, --accessed SECONDS
                        seconds from last access
  -p PATH, --path PATH  path for collect
  -t REGEX, --test-regex REGEX
                        test regex for each entry
