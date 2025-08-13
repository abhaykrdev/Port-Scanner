# Port-Scanner

A simple Port Scanner, script written in python. It scans ports on a specified IP address to determine if they are open or closed.

---

## Features

- **Multi-threaded scanning** — scans hundreds of ports in parallel for speed.
- **Banner grabbing** — fetches service information from open ports.
- **Verbose mode** — optional display of closed ports.
- **Custom port ranges** — scan exactly what you need.
- **Cross-platform** — works on Windows, macOS, and Linux.
- **Color-coded output** — easy-to-read terminal results using `colorama`.
- **Graceful exit** — handles `Ctrl+C` interrupts cleanly.

---

## 🛠 Requirements

- Python **3.7+**
- `colorama` package for colored terminal output
- Install colarama using `pip install colarama`

---

## 🏗 How It Works

1. **Validate target IP** → ensures valid IPv4 address.
2. **Thread-based scanning** → distributes ports among worker threads.
3. **TCP connection attempts** → determines port status (open/closed/filtered).
4. **Optional banner grabbing** → collects service identification strings.
5. **Output parsing** → displays results in a clean, color-coded format.
