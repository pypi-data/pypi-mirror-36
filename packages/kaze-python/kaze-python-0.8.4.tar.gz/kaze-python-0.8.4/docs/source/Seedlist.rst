kaze-Python SeedList
-------------------

Introduction
============
What is the SeedList?
"""""""""""""""""""""

The SeedList is a list of URLs belonging to the nodes that kaze-Python tries to connect to when it starts.
You can find the SeedList in ``protcol.*.json``, under in the kaze-python directory under ``/kaze/data``. Note that there are three commonly used ``protocol.*.json`` files:

::

    protocol.mainnet.json
    protocol.testnet.json
    protocol.privnet.json

This doc refers to ``protocol.mainnet.json`` but the information can be applied commonly.

::

    json
    {
        "ProtocolConfiguration": {
        "Magic": ...,
        "AddressVersion": ...,
        "SecondsPerBlock": ...,
        "StandbyValidators": [
        ...
        ],
        "SeedList": [
          "seed1.kaze.org:10333",
          "seed2.kaze.org:10333",
          "seed3.kaze.org:10333",
          "seed4.kaze.org:10333",
          "seed5.kaze.org:10333"
        ],
        "RPCList":[
        ...
        ],
        "SystemFee": {
        ...
        }
      }
    }
  
Here, kaze-Python is configured to connect to ``seed1.kaze.org``, ``seed2.kaze.org``, etc. through ``PORT:10333``.

Potential Problems
==================
What happens if every node in our list is down?

kaze-python is smart, so it will attempt to connect to neighbouring nodes. However, there are many unknown factors in this approach. Perhaps the neighbors are down. The wait time may be extended.

Updating a SeedList
===================
By updating the SeedList with addresses of nodes we are certain are alive, we can avoid lengthy wait times as described in **Potential Problems**.

Updating a Seedlist in kaze-Python using Windows WSL (Ubuntu)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
If you are running kaze-python using Ubuntu, you are mostly likely using a venv. Make sure to update the `protocol.mainnet.json` (as applicable) within your venv located at ``lib/python3.6/site-packages/kaze/data``.
If this path does not exist, you haven't used it in your current venv and you can edit the file located under your kaze-python folder at ``kaze/data``.
Alternatively, you could delete your venv folder, edit the parent file, make a new venv folder (``python -m venv venv``), activate your venv, then reinstall using ``pip install e .``.

How to update?
==============
Live nodes
""""""""""
How do we find out which nodes are alive? Use `kaze Network Status Monitor <http://monitor.KAZEBLOCKCHAIN.io/>`_.
If you would like more information visit the kaze Network Status Montior `repository <https://github.com/KAZEBLOCKCHAIN/kaze-mon>`_.


.. image:: ../seedlist.png
  :width: 400
  :alt: seedlist

A list of nodes that are available are shown above. The latest ones are pushed to the top.
*2* tells us if the node is responding. The preferable nodes are "up", which is indicated by the green color and "yes".

We follow this standard protocol for ports:

.. list-table:: Port Protocol
   :widths: 20 10 10
   :header-rows: 1
   
   * - 
     - Main Net
     - Test Net
   * - JSON-RPC via HTTPS
     - 10331
     - 20331
   * - JSON-RPC via HTTP 
     - 10332 
     - 20332
   * - P2P via TCP
     - 10333
     - 20333
   * - P2P via WebSocket
     - 10334
     - 20334

We will choose the first node over the third node, since *1* adheres the convention and *3* does not.

Therefore, we will choose the following live node addresses:

::

    seed3.aphelion-kaze.com
    seed4.aphelion-kaze.com
    node2.ams2.bridgeprotocol.io
    pyrpc1.nodekaze.ch
    node2.nyc3.bridgeprotocol.io


Editing the protocol
""""""""""""""""""""
To let kaze-Python know the new SeedList, we will paste the addresses chosen before into ``protocol.mainnet.json``
::

    json
    {
        "ProtocolConfiguration": {
        "Magic": ...,
        "AddressVersion": ...,
        "SecondsPerBlock": ...,
        "StandbyValidators": [
        ...
        ],
        "SeedList": [
          "seed1.kaze.org:10333",
          "seed2.kaze.org:10333",
          "seed3.kaze.org:10333",
          "seed4.kaze.org:10333",
          "seed5.kaze.org:10333",
          "seed4.aphelion-kaze.com:10333",
          "node2.sgp1.bridgeprotocol.io:10333",
          "seed2.aphelion-kaze.com:10333",
          "seed3.aphelion-kaze.com:10333",
          "node2.ams2.bridgeprotocol.io:10333",
          "pyrpc1.narrative.network:10333",
          "node2.nyc3.bridgeprotocol.io:10333",
          "pyrpc4.narrative.network:10333",
          "pyrpc2.narrative.network:10333",
          "pyrpc3.narrative.network:10333",
          "seed1.aphelion-kaze.com:10333",
          "seed1.switcheo.network:10333",
          "seed2.switcheo.network:10333",
          "seed5.KAZEBLOCKCHAIN.io:10333",
          "seed3.KAZEBLOCKCHAIN.io:10333",
          "seed3.switcheo.network:10333",
          "seed1.o3node.org:10333",
          "seed3.travala.com:10333",
          "seed4.KAZEBLOCKCHAIN.io:10333",
          "seed2.KAZEBLOCKCHAIN.io:10333",
          "seed2.o3node.org:10333",
          "seed3.o3node.org:10333",
          "node1.sgp1.bridgeprotocol.io:10333",
          "seed2.travala.com:10333",
          "seed4.switcheo.network:10333",
          "seed1.spotcoin.com:10333",
          "node1.nyc3.bridgeprotocol.io:10333"
        ],
        "RPCList":[
        ...
        ],
        "SystemFee": {
        ...
        }
      }
    }
  
Notice that we've added ``:10333`` to the end of each of the addresses, to tell kaze-Python to connect using the 'P2P' protocol.

You can now start kaze-python as usual.

JSON and REST API Servers
=========================

It is recommended that you update your seedlist prior to starting any API Servers to ensure maximum connections.
For more information about API Servers visit `here <https://kaze-python.readthedocs.io/en/latest/basicusage.html#api-server-json-and-or-rest>`_.
