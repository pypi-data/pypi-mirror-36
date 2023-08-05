# Continuous cURL

Continually test an endpoint over time, keeping track of http status codes.  Similar to ping -c but with curl.

## Motivation

When doing deployments or making critical infrastructure changes I like to get the quickest feedback possible on any failures.  Rather than wait a minute or so for Pingdom or Pagerduty to go off, I'd like to know within a second or two if health indicators start failing.  So I like to continually curl the health endpoint for any services I'm touching to make sure they continue to return 200's, else let me know right away.

## Installation

```shell
$ pip install ccurl
```

## Usage

```shell
# GET request on www.google.com 10 times
ccurl --url www.google.com --repeat 10

# GET request on www.google.com 100 times with a 2 second sleep between requests
ccurl --url www.google.com --repeat 100 --delay 2
```

## Publishing Updates to PyPi

For the maintainer - to publish an updated version of ssm-search, increment the version number in version.py and run the following:

```shell
docker build -f ./Dockerfile.buildenv -t ccurl:build .
docker run --rm -it --entrypoint make ccurl:build publish
```

At the prompts, enter the username and password to the pypi.org repo.

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
