from guillotina import configure


app_settings = {
    # provide custom application settings here...
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan('guillotina_linkintegrity.api')
    configure.scan('guillotina_linkintegrity.storage')
    configure.scan('guillotina_linkintegrity.subscribers')
