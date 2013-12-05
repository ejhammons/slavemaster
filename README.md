# Slavemaster

Slavemaster is a daemon, written in Python, that manages adding and deleting webheads from Lsync-based clusters.  

This is currently an alpha-level project.  Some work has been done to validate input, but there is still much work to be done and many features to be added and enhanced.

## Requirements
Slavemaster uses the bottle framework available through pip with ```pip install bottle``` or at <http://bottlepy.org>

The provided Lsyncd configuration is designed for use with Lsyncd 2.1.4, but should be compatible with later versions.

## Installation

Install Lsyncd on the master server and configure it using the example provided.  By default, the list of slaves is stored in /etc/lsyncd/servers.conf.  List the servers, one per line, in this file either by IP address or locally-resolvable hostname.  

Run slavemaster.py on the master.  Currently there are no sysv or upstart files, these are planned to be added in the future.  The server listens on port 5143 for api requests.  The server must be run as root, or a user with read/write access to the servers.conf file and access to the service command.

## Usage

Currently, the following calls are supported:

GET /list Returns a list of slave servers

POST /add Adds a server to the list.  The server expects a JSON object as data consisting of a list with a single string containing the server's IP or hostname to be added.  Returns the resulting list of servers.

POST /delete Deletes a server from the list.  The server expects a JSON object as data consisting of a list with a single string containing the server's IP or hostname to be deleted.  Returns the resulting list of servers.

GET /restart-lsyncd Restarts the lsyncd service on the master to reread the server list.

## Examples

```
curl http://10.1.1.1:5143/list
```
Lists the current servers

```
curl -X POST -H "Content-type: application/json" http://10.1.1.1:5143/add -d'["10.1.1.2"]'
```
Adds 10.1.1.2 to the list

```
curl -X POST -H "Content-type: application/json" http://10.1.1.1:5143/delete -d'["10.1.1.2"]'
```
Deletes 10.1.1.2 from the list

```
curl http://10.1.1.1:5143/restart-lsyncd
```
Restarts lsyncd to read the current list of servers

