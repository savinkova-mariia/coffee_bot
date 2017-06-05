
from channels import route
from posts.consumers import connect_table, disconnect_table, save_post

channel_routing = [
    # Called when incoming WebSockets connect
    route("websocket.connect", connect_table, path=r'^/tables/(?P<slug>[^/]+)/stream/$'),

    # Called when the client closes the socket
    route("websocket.disconnect", disconnect_table, path=r'^/tables/(?P<slug>[^/]+)/stream/$'),

    # Called when the client sends message on the WebSocket
    route("websocket.receive", save_post, path=r'^/tables/(?P<slug>[^/]+)/stream/$'),

]