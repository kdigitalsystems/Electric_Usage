# Kasa Energy Logger ⚡

This project automates the tracking of electricity usage from a TP-Link Kasa smart device. It retrieves energy consumption data and logs it (e.g., to a CSV file) to build a continuous dataset of daily electricity usage. 

Because local network access is required to communicate with the Kasa device, this project utilizes a **Self-Hosted GitHub Actions Runner** to execute scheduled cron jobs directly from a local machine (like a Raspberry Pi or home server).

## 🚀 Features
* Automatically fetches energy usage from Kasa smart plugs/devices.
* Appends daily usage statistics to a continuous log file.
* Runs fully automated via GitHub Actions on a local self-hosted runner.

## 🛠️ Project Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/Electric_Usage_K_Digital_Systems_LLC.git](https://github.com/yourusername/Electric_Usage_K_Digital_Systems_LLC.git)
   cd Electric_Usage_K_Digital_Systems_LLC
   ```

2. **Install dependencies:**
   Ensure you have Python 3 installed, then install the required packages (such as `python-kasa`):
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Self-Hosted Runner Setup

To allow GitHub Actions to access your local Kasa device, you must configure a self-hosted runner on a machine connected to the same network.

### 1. Download and Extract
Run these commands in your terminal to create the runner folder and download the software:

```bash
# Create a folder for the runner
mkdir actions-runner && cd actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.333.1.tar.gz -L [https://github.com/actions/runner/releases/download/v2.333.1/actions-runner-linux-x64-2.333.1.tar.gz](https://github.com/actions/runner/releases/download/v2.333.1/actions-runner-linux-x64-2.333.1.tar.gz)

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.333.1.tar.gz
```

### 2. Configure
Link the runner to your GitHub repository using your specific configuration token:

```bash
./config.sh --url [https://github.com/yourusername/Electric_Usage_K_Digital_Systems_LLC](https://github.com/yourusername/Electric_Usage_K_Digital_Systems_LLC) --token YOUR_GITHUB_TOKEN_HERE
```
*(Follow the on-screen prompts to set the runner name and labels. The default labels usually include `self-hosted`.)*

---

## 🔄 Running as a Background Service

To ensure the runner stays active even if you close your terminal or reboot the machine, configure it as a background system service using the built-in `svc.sh` script.

### Install and Start the Service
Make sure you are inside your `actions-runner` directory, then run:

```bash
# Install the service (requires sudo)
sudo ./svc.sh install

# Start the service
sudo ./svc.sh start
```

### Managing the Service
You can check the status of your runner or stop it at any time using the following commands:

* **Check Status:** ```bash
  sudo ./svc.sh status
  ```
  *(This will output whether the service is `active (running)`, `inactive`, or `failed`.)*

* **Stop the Runner:**
  ```bash
  sudo ./svc.sh stop
  ```

* **Uninstall the Service:**
  ```bash
  sudo ./svc.sh uninstall
  ```
  *(Note: You must stop the service before uninstalling it).*
