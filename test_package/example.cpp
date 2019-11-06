#include <sio_client.h>

#ifdef SIO_TLS
#include <boost/asio/ssl/context.hpp>
#endif

int main() {
#ifdef SIO_TLS
  using boost::asio::ssl::context;
  context ctx{context::tlsv12_client};
  sio::client c{ctx};
#else
  sio::client c;
#endif
}
