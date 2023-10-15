# Instructions to run the project in Linux

### Install pip3

> python3 -m pip install --user --upgrade pip

### Installing virtualenv

> python3 -m pip install --user virtualenv

### Creating a virtual environment¶

> python3 -m venv env

### Activating a virtual environment¶

> source env/bin/activate

### Installing packages

> python3 -m pip install -r requirements.txt

`Resources/config.json`

```
{
  "browser": "chrome",
  "arguments": [
    "--start-maximized",
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
  ],
  "experimental_options": [
    ["prefs", { "download.default_directory": "./Resources/" }],
    ["excludeSwitches", ["enable-automation"]],
    ["useAutomationExtension", false]
  ],
  "wait_time": 10
}
```

`Resrouces/data.json`

```
{
  "start_url": "https://some_flight_website",
  "flights_input_file": "./Resources/Book1.xlsx",
  "flights_output_file": "./Resources/output.xlsx"
}
```

#### Excel File Information

Column Status:

    0 is PENDING

    1 is COMPLETED

    2 is DATA_ERROR

    3 is SCRAPE_ERROR

## RUN PROJECT

> python3 main.py

# ATTENTION:

### Make sure you have filled `data.json` and `config.json`
