# Advanced Socket Programming in C on Linux
## 10-Slide PowerPoint Content
### Topic: Blocking, Non-Blocking, `select()`, `epoll()` with Sample TCP Server & Client

---

## Slide 1: Title Slide
**Advanced Socket Programming in C on Linux**  
**Blocking, Non-Blocking, `select()`, and `epoll()`**  
**With Sample TCP Server & Client**

- Presented by: Shubham
- Language: C
- Platform: Linux OS

---

## Slide 2: Introduction to Socket Programming
- Socket programming enables communication between two processes over a network.
- A socket acts as an endpoint for sending and receiving data.
- In Linux, sockets are represented as file descriptors.
- Common use cases:
  - Client-server applications
  - Chat applications
  - Web servers
  - File transfer tools

---

## Slide 3: TCP Client-Server Model
**Server-side flow:**
- `socket()`
- `bind()`
- `listen()`
- `accept()`
- `recv()` / `send()`
- `close()`

**Client-side flow:**
- `socket()`
- `connect()`
- `send()` / `recv()`
- `close()`

**Why TCP?**
- Reliable communication
- Ordered data delivery
- Connection-oriented protocol

---

## Slide 4: Sample TCP Server (C)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE] = {0};

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(server_fd, 5);
    client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
    recv(client_fd, buffer, BUFFER_SIZE, 0);
    printf("Client says: %s\n", buffer);
    send(client_fd, "Hello from server", 17, 0);

    close(client_fd);
    close(server_fd);
    return 0;
}
```

---

## Slide 5: Sample TCP Client (C)
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE] = {0};

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    send(sockfd, "Hello from client", 17, 0);
    recv(sockfd, buffer, BUFFER_SIZE, 0);
    printf("Server replied: %s\n", buffer);

    close(sockfd);
    return 0;
}
```

---

## Slide 6: Blocking I/O
- In blocking mode, a socket call waits until the operation completes.
- Example:
  - `accept()` waits until a client connects
  - `recv()` waits until data arrives
- Advantages:
  - Simple and easy to understand
- Disadvantages:
  - Poor performance for multiple clients
  - One blocked call can delay the program

**Example:**
```c
int client_fd = accept(server_fd, NULL, NULL);
recv(client_fd, buffer, sizeof(buffer), 0);
```

---

## Slide 7: Non-Blocking I/O
- In non-blocking mode, socket calls return immediately.
- If data is unavailable, the call returns `EAGAIN` or `EWOULDBLOCK`.
- Useful for responsive and event-driven applications.

**Enable non-blocking mode:**
```c
#include <fcntl.h>
int flags = fcntl(sockfd, F_GETFL, 0);
fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);
```

**Benefit:**
- Program can continue doing other work without waiting.

---

## Slide 8: `select()` for I/O Multiplexing
- `select()` monitors multiple file descriptors at the same time.
- It tells which sockets are ready for reading or writing.
- Good for small multi-client servers.

**Prototype:**
```c
int select(int nfds, fd_set *readfds, fd_set *writefds,
           fd_set *exceptfds, struct timeval *timeout);
```

**Key macros:**
- `FD_ZERO()`
- `FD_SET()`
- `FD_ISSET()`

**Limitation:**
- Slower when handling many file descriptors.

---

## Slide 9: `epoll()` for Scalable Event Handling
- `epoll()` is a Linux-specific mechanism for monitoring many file descriptors efficiently.
- Better than `select()` for large-scale servers.

**Main functions:**
- `epoll_create1()`
- `epoll_ctl()`
- `epoll_wait()`

**Why use `epoll()`?**
- High performance
- Scales to thousands of connections
- Processes only active sockets

---

## Slide 10: Comparison and Conclusion
### Blocking vs Non-Blocking vs `select()` vs `epoll()`

| Method | Best For | Limitation |
|---|---|---|
| Blocking | Simple programs | Waits on each operation |
| Non-Blocking | Responsive apps | More complex logic |
| `select()` | Small multi-client apps | FD limit, slower scaling |
| `epoll()` | Large Linux servers | Linux-specific |

### Conclusion
- Blocking I/O is simple but limited.
- Non-blocking I/O improves responsiveness.
- `select()` supports multiple clients.
- `epoll()` is best for scalable Linux server applications.

**Thank You / Q&A**
