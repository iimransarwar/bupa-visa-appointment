# Appointment Scraper

This Python script scrapes appointment availability from the Bupa Medical Visa Services website (`https://bmvs.onlineappointmentscheduling.net.au/oasis/Default.aspx`) for a given postcode (default: 5000) and outputs details for locations within 50 km that have available slots. The script runs in headless mode (no visible browser UI) and outputs only the appointment details in a clean format.

## Features
- Scrapes location, address, distance, and availability of appointments.
- Outputs results in a concise format with an ACST timestamp.
- Runs in the background using Chrome in headless mode.
- Supports macOS (ARM and Intel) and Windows.
- Includes error handling with page source logging for debugging.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **Google Chrome**: The script uses Chrome for web scraping.
- **ChromeDriver**: Must match your Chrome version.
- **Required Python packages**:
  - `selenium`
  - `beautifulsoup4`
  - `pytz`

## Installation

### macOS (ARM or Intel)

1. **Install Python**:
   - Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/).
   - Verify installation:
     ```bash
     python3 --version
     ```

2. **Install Google Chrome**:
   - Download and install Google Chrome from [google.com/chrome](https://www.google.com/chrome/).
   - Verify Chrome is installed at:
     - ARM: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
     - Intel: Same path, but ensure compatibility with your system.

3. **Install ChromeDriver**:
   - Check your Chrome version:
     - Open Chrome, go to `About Chrome` (chrome://settings/help).
   - Download the matching ChromeDriver version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).
   - For ARM Mac:
     - Place the `chromedriver` executable in `/opt/homebrew/Caskroom/chromedriver/<version>/chromedriver-mac-arm64/chromedriver`.
     - Example: `/opt/homebrew/Caskroom/chromedriver/138.0.7204.92/chromedriver-mac-arm64/chromedriver`.
   - For Intel Mac:
     - Place in `/opt/homebrew/Caskroom/chromedriver/<version>/chromedriver-mac-x64/chromedriver` or `/usr/local/bin/chromedriver`.
   - Make executable:
     ```bash
     chmod +x /path/to/chromedriver
     ```
   - If placed in `/usr/local/bin`, the script will find it automatically.

4. **Install Python Packages**:
   - Install required packages using pip:
     ```bash
     pip3 install selenium beautifulsoup4 pytz
     ```

5. **Clone or Download the Script**:
   - Save the script as `filter_appointments_headless.py` in your working directory.

### Windows

1. **Install Python**:
   - Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/).
   - Ensure `Add Python to PATH` is checked during installation.
   - Verify installation:
     ```cmd
     python --version
     ```

2. **Install Google Chrome**:
   - Download and install Google Chrome from [google.com/chrome](https://www.google.com/chrome/).
   - Verify Chrome is installed at:
     - Default: `C:\Program Files\Google\Chrome\Application\chrome.exe`

3. **Install ChromeDriver**:
   - Check your Chrome version:
     - Open Chrome, go to `About Chrome` (chrome://settings/help).
   - Download the matching ChromeDriver version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).
   - Extract `chromedriver.exe` and place it in:
     - Example: `C:\chromedriver\chromedriver.exe`
   - Add the directory to your system PATH:
     - Right-click `This PC` > `Properties` > `Advanced system settings` > `Environment Variables`.
     - Under `System Variables`, edit `Path` and add the directory (e.g., `C:\chromedriver`).
   - Alternatively, update the script’s `chromedriver_path` to the full path:
     ```python
     chromedriver_path = "C:/chromedriver/chromedriver.exe"
     ```

4. **Install Python Packages**:
   - Install required packages using pip:
     ```cmd
     pip install selenium beautifulsoup4 pytz
     ```

5. **Clone or Download the Script**:
   - Save the script as `filter_appointments_headless.py` in your working directory.

## Running the Script

### macOS

1. **Navigate to the Script Directory**:
   ```bash
   cd /path/to/script/directory
   ```

2. **Run the Script**:
   ```bash
   python3 filter_appointments_headless.py
   ```
   - The script runs in the background (no browser UI) and outputs appointment details to the terminal.
   - Example output:
     ```
     2025-07-02 15:16:03,703 - INFO - Found available appointments
     Location: Adelaide
     Address: Adelaide - Bupa CentreLevel 1 151 Pirie StAdelaide
     Distance: 1 km
     Availability: Sunday 06/07/202508:45 AM
     --------------------------------------------------
     Location: Royal Park
     Address: Old Port Road Medical & Dental Centre 1202 Old Port Road Royal Park SA 5014
     Distance: 12 km
     Availability: Wednesday 16/07/202510:15 AM
     --------------------------------------------------
     ```

3. **Run in Background** (Optional):
   - To run without keeping the terminal open:
     ```bash
     python3 filter_appointments_headless.py > output.txt 2>&1 &
     ```
   - Check `output.txt` for results.

### Windows

1. **Navigate to the Script Directory**:
   ```cmd
   cd C:\path\to\script\directory
   ```

2. **Run the Script**:
   ```cmd
   python filter_appointments_headless.py
   ```
   - The script runs in the background (no browser UI) and outputs appointment details to the Command Prompt.
   - Example output is the same as above.

3. **Run in Background** (Optional):
   - To run without keeping the Command Prompt open:
     ```cmd
     start /b python filter_appointments_headless.py > output.txt 2>&1
     ```
   - Check `output.txt` for results.

## Configuration

- **Postcode**: The script uses postcode `5000` by default. To change it, modify the line:
  ```python
  location_input.send_keys("5000")
  ```
  Replace `"5000"` with your desired postcode.

- **Distance Filter**: The script filters locations within 50 km. To change this, modify:
  ```python
  if distance < 50:
  ```
  Adjust `50` to your preferred distance.

- **ChromeDriver Path**: If ChromeDriver is not in PATH, update:
  ```python
  chromedriver_path = "/path/to/chromedriver"
  ```
  - macOS example: `/opt/homebrew/Caskroom/chromedriver/138.0.7204.92/chromedriver-mac-arm64/chromedriver`
  - Windows example: `C:/chromedriver/chromedriver.exe`

- **Chrome Binary**: If Chrome is installed in a non-standard location, update:
  ```python
  chrome_options.binary_location = "/path/to/chrome"
  ```
  - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
  - Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`

## Troubleshooting

- **ChromeDriver Version Mismatch**:
  - Ensure ChromeDriver matches your Chrome version (check `chrome://settings/help`).
  - Download the correct version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).

- **Script Errors**:
  - If the script fails, check `page_source.html` in the script directory for the page source at the time of failure.
  - Temporarily enable debug logs by changing `logging.basicConfig(level=logging.ERROR)` to `logging.basicConfig(level=logging.DEBUG)`.

- **No Output**:
  - Verify the website URL and HTML structure haven’t changed.
  - Ensure internet connectivity and the postcode is valid.

- **Headless Mode Issues**:
  - If headless mode fails, comment out `chrome_options.add_argument("--headless=new")` to run with a visible browser for debugging.

## Notes
- The script uses the ACST timezone (`Australia/Adelaide`) for timestamps.
- Only locations with available appointment slots within 50 km are displayed.
- The script is optimized for performance with `--disable-images` and `--disable-extensions`. Remove these options if the website requires images or extensions.
