# Anomaly Detection Application

This application is designed to detect anomalies related to tips in a database. It generates a log file that contains detailed information for each tip with an associated identity. For each tip, the log file will include a row with the following data: the internal tip identifier, creation date, update date, the length of the encrypted JSON identity, the existence of an access request, whether the access request is authorized, the tip status, and a flag indicating a possible anomaly.

## Prerequisites

Ensure that you have Python installed on your system. You can download Python from [here](https://www.python.org/downloads/).

## Setting Up the Application

1. **Create a Python Virtual Environment**

    Navigate to the cloned repository and create a virtual environment. This keeps dependencies required by the project separate from your global Python environment.

    ```bash
    cd <repository-folder>
    python -m venv venv
    ```

2. **Activate the Virtual Environment**

    - On Windows, activate the virtual environment using:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS or Linux, use:

        ```bash
        source venv/bin/activate
        ```

3. **Install Dependencies**

    With the virtual environment activated, install the required dependencies using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Collect Data**

    First, the application processes data from a specified database. Ensure that your database file (`<database>.db`) is accessible to the application and contains the relevant data structures.

2. **Run the Anomaly Detection**

    Execute the following command to start the anomaly detection process and output the log file:

    ```bash
    python anomaly_detection.py <database>.db <logfile>.csv
    ```

    The generated `<logfile>.csv` will contain rows of data with the following structure:

    | internaltip_id | creation_date | update_date | identity_length | access_request_exists | access_request_authorized | status | anomaly_flag |
    | -------------- | ------------- | ----------- | --------------- | --------------------- | ------------------------- | ------ | ------------ |
    | int_tip_id_1   | YYYY-MM-DD    | YYYY-MM-DD  | length_in_bytes | Yes/No                | Yes/No                    | Status | Yes/No       |
    | ...            | ...           | ...         | ...             | ...                   | ...                       | ...    | ...          |

    Note: `identity_length` represents the length of the encrypted JSON identity data.

After the program finishes execution, you can review the `<logfile>.csv` for detailed analysis and further investigation of any anomalies detected.