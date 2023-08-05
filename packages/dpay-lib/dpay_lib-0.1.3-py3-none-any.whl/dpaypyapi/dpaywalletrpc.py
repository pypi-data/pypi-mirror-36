from grapheneapi.grapheneapi import GrapheneAPI


class DPayWalletRPC(GrapheneAPI):
    """ dPay JSON-HTTP-RPC API

        This class serves as an abstraction layer for easy use of the
        Grapehene API.

        :param str host: Host of the API server
        :param int port: Port to connect to
        :param str username: Username for Authentication (if required,
                             defaults to "")
        :param str password: Password for Authentication (if required,
                             defaults to "")

        All RPC commands of the dpay client are exposed as methods
        in the class ``DPayWalletRPC``. Once an instance of DPayWalletRPC is
        created with host, port, username, and password, e.g.,

        .. code-block:: python

            from dpaypyrpc import DPayRPC
            rpc = DPayRPC("localhost", 8092, "", "")

        any call available to that port can be issued using the instance
        via the syntax rpc.*command*(*parameters*). Example:

        .. code-block:: python

            rpc.info()

        .. note:: A distinction has to be made whether the connection is
                  made to a **witness/full node** which handles the
                  blockchain and P2P network, or a **cli-wallet** that
                  handles wallet related actions! The available commands
                  differ drastically!

        If you are connected to a wallet, you can simply initiate a transfer with:

        .. code-block:: python

            res = client.transfer("sender","receiver","5", "USD", "memo", True);

        Again, the witness node does not offer access to construct any transactions,
        and hence the calls available to the witness-rpc can be seen as read-only for
        the blockchain.
    """
    def __init__(self, *args, **kwargs):
        super(DPayWalletRPC, self).__init__(*args, **kwargs)
