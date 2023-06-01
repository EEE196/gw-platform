#include <libwebsockets.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static struct lws *client_wsi = NULL;
static int connection_established = 0;

// WebSocket callback function
static int callback(struct lws *wsi, enum lws_callback_reasons reason,
                    void *user, void *in, size_t len)
{
    switch (reason) {
        case LWS_CALLBACK_CLIENT_ESTABLISHED:
            printf("WebSocket connection established.\n");
            connection_established = 1;
            break;

        case LWS_CALLBACK_CLIENT_RECEIVE:
            // Process received message
            printf("Received message from server: %.*s\n", (int)len, (char *)in);
            break;

        case LWS_CALLBACK_CLIENT_WRITEABLE:
            // Send a message to the server
            if (connection_established) {
                char *message = "Hello, server!";
                int message_len = strlen(message);
                lws_write(client_wsi, (unsigned char *)message, message_len, LWS_WRITE_TEXT);
            }
            break;

        case LWS_CALLBACK_CLOSED:
            printf("WebSocket connection closed.\n");
            lws_context_destroy(wsi->context);
            break;

        default:
            break;
    }

    return 0;
}

int main(void)
{
    struct lws_context_creation_info info;
    struct lws_client_connect_info ccinfo;
    struct lws_protocols protocol;
    struct lws_context *context;
    const char *address = "localhost";
    int port = 8080;
    const char *path = "/";
    const char *origin = "origin";

    memset(&info, 0, sizeof(info));
    memset(&ccinfo, 0, sizeof(ccinfo));
    memset(&protocol, 0, sizeof(protocol));

    protocol.name = "my-protocol";
    protocol.callback = callback;

