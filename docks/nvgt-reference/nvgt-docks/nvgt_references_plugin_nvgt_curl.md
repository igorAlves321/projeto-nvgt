# nvgt_curl
## classes
### internet_request
#### properties
##### bytes_downloaded
The number of bytes currently downloaded with this internet_request.

`double internet_request::bytes_downloaded;`


##### bytes_uploaded
The number of bytes that have been uploaded with this internet_request.

`double internet_request::bytes_uploaded;`


##### complete
Determine if the active request has completed yet or not.

`bool internet_request::complete;`


##### download_percent
The current percentage downloaded.

`double internet_request::download_percent;`


##### download_size
The size of the data you're downloading (in bytes).

`double internet_request::download_size;`


##### follow_redirects
Should your request follow HTTP redirects?

`bool internet_request::follow_redirects;`


##### in_progress
Determine if the request is currently in progress.

`bool internet_request::in_progress;`


##### max_redirects
The maximum number of redirects to perform before giving up.

`int internet_request::max_redirects;`


##### no_curl
Tells you if libcurl was successfully able to initialize this request, do not use this object if this property is false!

`bool no_curl;`


##### status_code
Represents the HTTP status code returned by this request.

`int internet_request::status_code;`


##### upload_percent
The percentage uploaded.

`double internet_request::upload_percent;`


##### upload_size
The size of your upload (in bytes).

`double internet_request::upload_size;`





## functions
### curl_url_decode
Decode an encoded URL using curl.

`string curl_url_decode(string url);`

#### Arguments:
* string url: the URL to decode.

#### Returns:
string: the decoded URL.

#### Remarks:
This functionality exists natively in NVGT too, the curl functions are just provided here for completeness. For more information, see the built-in `url_decode()` function.


### curl_url_encode
Encode a URL using curl.

`string curl_url_encode(string url);`

#### Arguments:
* string url: the URL to encode.

#### Returns:
string: the encoded URL.

#### Remarks:
This functionality exists natively in NVGT too, the curl functions are just provided here for completeness. For more information, see the built-in `url_encode()` function.




