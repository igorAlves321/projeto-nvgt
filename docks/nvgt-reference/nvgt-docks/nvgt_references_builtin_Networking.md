# Networking
## classes
### http

Facilitate HTTP requests from a simple, asynchronous interface.

http();

#### Remarks:

This is one of the easiest ways to perform an http request in NVGT without blocking the rest of your code.

Simply create an http object, call either it's get, head or post methods, then begin accessing properties on the object such  as progress, status_code or response_body to query and access details of the request.

#### Example:

```NVGT
#include "size.nvgt"
#include "speech.nvgt"
void main() {
	// This script downloads the latest NVGT windows installer and saves it in the current working directory.
	http h;
	h.get("https://nvgt.zip/windows");
	file f;
	string filename = "";
	show_window("downloading...");
	while (!h.complete) {
		wait(5);
		if (key_pressed(KEY_ESCAPE)) {
			f.close();
			file_delete(filename);
			return; // Destruction of the http object will cancel any requests in progress.
		}
		if (!f.active and h.status_code == 200) { // The file is available.
			string[]@ path = h.url.get_path_segments();
			filename = path.length() > 0? path[-1] : "http.txt";
			f.open(filename, "wb");
		}
		if (f.active) f.write(h.response_body);
		if (key_pressed(KEY_SPACE)) speak(round(h.progress * 100, 2) + "%");
	}
	int keep = question(filename, size_to_string(f.size) + " downloaded, keep file?");
	f.close();
	if (keep != 1) file_delete(filename);
}
```



#### Methods
##### get

Initiate a get request.

bool get(spec::uri url, name_value_collection@ headers = null, http_credentials@ creds = null);

###### Arguments:

* spec::uri url: A valid URI which must have a scheme of either http or https.

* name_value_collection@ headers = null: Pairs of extra http headers to pass on to the server.

* http_credentials@ creds = null: Optional credentials to authenticate the request with.

###### Returns:

bool: True if the request was initiated, or false if there was an error.

###### Remarks:

Once this method is called and returns true, you will usually want to wait until either http.complete returns true or http.running returns false before thoroughly handling the request. However http.progress, http.status_code, http.response_headers and http.response_body are accessible throughout the request's lifecycle to stream the data or get more detailed information.

###### Example:

```NVGT
void main() {
	// Fetch the latest version of NVGT.
	http h;
	if (!h.get("http://nvgt.dev/downloads/latest_version")) {
		alert("oops", "request failed"); // This class will contain more detailed error management facilities in the near future.
		return;
	}
	h.wait(); // You can also use the h.running or h.complete properties in a loop to execute code in the background while the request progresses.
	alert("nvgt latest version", h.response_body);
}
```



##### reset

Resets the http object to the state it was in at the time of it's construction, canceling any requests in progress.

void reset();

###### Remarks:

This method waits for the current request to cancel successfully, which is usually instant. However from time to time you could see a small delay as the request thread runs to the next point where it can check the cancelation event.

This method is implicitly called whenever the http object destructs.

###### Example:

```NVGT
void main() {
	http h;
	h.get("https://nvgt.dev");
	wait(20);
	h.reset();
	h.get("https://samtupy.com/ip.php");
	h.wait();
	if (h.status_code != 200) alert("oops " + h.status_code, h.response_body);
	else alert("IP address displayed after http reset", h.response_body);
}
```



##### wait
Waits for the current request to complete.

`void wait();`

###### Remarks:
If no request is in progress, this will return emmedietly. Otherwise, it will block code execution on the calling thread until the request has finished.



#### Properties
##### progress
Determine the percentage of the request download (from 0.0 to 1.0.

`const float progress;`

###### Remarks:
This property will be 0 if a request is not in progress or if it is not yet in a state where the content length of the download can be known, and -1 if the progress cannot be determined such as if the remote endpoint does not provide a Content-Length header.


##### response_body
Read and consume any new data from the current request.

`const string response_body;`

###### Remarks:
It is important to note that accessing this property will flush the buffer stored in the request. This means that for example you do not want to access http.response_body.length(); because the next time http.response_body is accessed it will be empty or might contain new data.

Proper usage is to continuously append the value of this property to a string or datastream in a loop while h.running is true or h.complete is false.




### network
#### methods
##### connect
Attempt to establish a connection with a server, only works when set up as a client.

`uint64 network::connect(const string&in hostname, uint16 port);`

###### Arguments:
* const string&in hostname: the hostname/IP address to connect to.
* uint16 port: the port to use.

###### Returns:
uint64: the peer ID of the connection, or 0 on error.


##### destroy
Destroys the network object, freeing all its resources, active connections, etc.

`void network::destroy();`


##### disconnect_peer
Tell a peer to disconnect and completely disregard its message queue. This means that the peer will be told to disconnect without sending any of its queued packets (if any).

`bool network::disconnect_peer(uint peer_id);`

###### Arguments:
* uint peer_id: the ID of the peer to disconnect.

###### Returns:
bool: true on success, false otherwise.


##### disconnect_peer_forcefully
Forcefully disconnect a peer. Unlike `network::disconnect_peer()`, this function doesn't send any sort of notification of the disconnection to the remote peer, instead it closes the connection immediately.

`bool network::disconnect_peer_forcefully(uint peer_id);`

###### Arguments:
* uint peer_id: the ID of the peer to disconnect.

###### Returns:
bool: true on success, false otherwise.


##### disconnect_peer_softly
Send a disconnect packet for a peer after sending any remaining packets in the queue and notifying the peer.

`bool network::disconnect_peer_softly(uint peer_id);`

###### Arguments:
* uint peer_id: the ID of the peer to disconnect.

###### Returns:
bool: true on success, false otherwise.


##### get_peer_address
Returns the IP address of a particular peer.

`string network::get_peer_address(uint peer_id);`

###### Arguments:
* uint peer_id: the ID of the peer to check.

###### Returns:
string: the IP address of the specified peer.


##### get_peer_list
Return a list of all peer ID's currently connected to the server.

`uint[]@ network::get_peer_list();`

###### Returns:
uint[]@: a handle to an array containing the ID of every peer currently connected to the server.


##### request
This is the function you'll probably be calling the most when you're dealing with the network object in NVGT. It checks if an event has occurred since the last time it checked. If it has, it returns you a network_event handle with info about it.

`network_event@ network::request(uint timeout = 0);`

###### Arguments:
* uint timeout = 0: an optional timeout on your packet receiving (see remarks for more information).

###### Returns:
network_event@: a handle to a `network_event` object containing info about the last received event.

###### Remarks:
The timeout parameter is in milliseconds, and it determines how long Enet will wait for new packets before returning control back to the calling application. However, if it receives a packet within the timeout period, it will return and you'll be handed the packet straight away.


##### send
Attempt to send a packet over the network.

`bool network::send(uint peer_id, const string&in message, uint8 channel, bool reliable = true);`

###### Arguments:
* uint peer_id: the ID of the peer to send to (specify 1 to send to the server from a client).
* const string&in message: the message to send.
* uint8 channel: the channel to send the message on (see the main networking documentation for more details).
* bool reliable = true: whether or not the packet should be sent reliably or not (see the main networking documentation for more details).

###### Returns:
bool: true if the packet was successfully sent, false otherwise.


##### send_reliable
Attempt to send a packet over the network reliably.

`bool network::send_reliable(uint peer_id, const string&in message, uint8 channel);`

###### Arguments:
* uint peer_id: the ID of the peer to send to (specify 1 to send to the server from a client).
* const string&in message: the message to send.
* uint8 channel: the channel to send the message on (see the main networking documentation for more details).

###### Returns:
bool: true if the packet was successfully sent, false otherwise.


##### send_unreliable
Attempt to send a packet over the network unreliably.

`bool network::send_unreliable(uint peer_id, const string&in message, uint8 channel);`

###### Arguments:
* uint peer_id: the ID of the peer to send to (specify 1 to send to the server from a client).
* const string&in message: the message to send.
* uint8 channel: the channel to send the message on (see the main networking documentation for more details).

###### Returns:
bool: true if the packet was successfully sent, false otherwise.


##### set_bandwidth_limits
Set the incoming and outgoing bandwidth limits of the server (in bytes-per-second).

`void network::set_bandwidth_limits(uint incoming, uint outgoing);`

###### Arguments:
* uint incoming: the maximum number of allowed incoming bytes per second.
* uint outgoing: the maximum number of allowed outgoing bytes per second.


##### setup_client
Sets up the network object as a client.

`bool network::setup_client(uint8 max_channels, uint16 max_peers);`

###### Arguments:
* uint8 max_channels: the maximum number of channels used on the connection (up to 255).
* uint16 max_peers: the maximum number of peers allowed by the connection (maximum is 65535).

###### Returns:
bool: true if the client was successfully set up, false otherwise.


##### setup_local_server
Sets up the network object as a local server on localhost.

`bool network::setup_local_server(uint16 bind_port, uint8 max_channels, uint16 max_peers);`

###### Arguments:
* uint16 bind_port: the port to bind the server to.
* uint8 max_channels: the maximum number of channels used on the connection (up to 255).
* uint16 max_peers: the maximum number of peers allowed by the connection (maximum is 65535).

###### Returns:
bool: true if the server was successfully set up, false otherwise.


##### setup_server
Sets up the network object as a server.

`bool network::setup_server(uint16 bind_port, uint8 max_channels, uint16 max_peers);`

###### Arguments:
* uint16 bind_port: the port to bind the server to.
* uint8 max_channels: the maximum number of channels used on the connection (up to 255).
* uint16 max_peers: the maximum number of peers allowed by the connection (maximum is 65535).

###### Returns:
bool: true if the server was successfully set up, false otherwise.



#### properties
##### active
Determine if the network object is active (e.g. a setup_* method has successfully been called on it).

`bool network::active;`


##### bytes_received
The number of bytes this network object has received since being set up.

`uint network::bytes_received;`


##### bytes_sent
The number of bytes this network object has sent since being set up.

`uint network::bytes_sent;`


##### connected_peers
The number of peers currently connected to the server.

`uint network::connected_peers;`




### network_event
This class represents an event received with the network object's `request()` method. It contains information such as the the ID of the peer that sent the event, the message the event was sent on, and the actual packet data itself.


#### methods
##### opAssign
This class implements the `opAssign()` operator overload, meaning it can be assigned with the "=" operator to another network_event.

`network_event@ opAssign(network_event@ e);`



#### properties
##### channel
The channel this event was sent on. See the main networking documentation for more information.

`uint network_event::channel;`


##### message
The data associated with this event (AKA the packet).

`string network_event::message;`


##### peer_id
The peer ID of the connection this event came from. See the main networking documentation for more information.

`uint network_event::peer_id;`


##### type
The type of the network event (see event types for more information).

`int network_event::type;`





## Constants
### Event Types

This is a list of all the constants supported as event types by NVGT's networking layer.

- event_none: no event.
- event_connect: a new user wants to connect.
- event_disconnect: a user wants to disconnect.
- event_receive: a user sent a packet.




