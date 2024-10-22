# AsRecordedAPP

## Description

**AsRecordedAPP** is a dialogue management and data collection application that facilitates the organization and editing of information in Excel sheets. This application is built using PyQt5 for the graphical user interface and Pandas for data manipulation in Excel.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Load and view Excel sheets**: Allows loading any Excel file and viewing its content within the application.
- **Filter and search characters and dialogues**: Quickly search through dialogues and characters using an advanced filter.
- **Mark interventions as complete**: An option to track progress by marking dialogues as complete.
- **Edit and save changes in Excel**: Changes are saved directly in the original file, making the workflow easier.
- **Navigation between takes and characters**: Easy and fast navigation between different takes, with the ability to filter by character.

## Project Structure

```plaintext
AsRecordedAPP/
├── datahandler/
│   ├── __init__.py
│   ├── data_handler.py
│   ├── data_validator.py
│   ├── excel_handler.py
│   └── exceptions.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── main_widget.py
│   ├── gidoia_widget.py
│   ├── character_filter_dialog.py
│   ├── custom_widgets.py
│   └── utils.py
├── resources/
│   └── main.css
├── PreparacionExcel/
│   ├── Excel/
│   │   └── Example Excel
│   ├── scripts/
│   │   ├── CrearTxt.py  # Creates a suitable txt for the program using the reference word
│   │   └── PandasGuion.py  # Creates the xlsx using the reference txt
│   ├── Txt/
│   │   └── Example Txt  # Recommended as a template to work with the program
│   └── Word/
│       └── Example Word  # Specific to the program used by the company
├── main.py
└── README.md
```

## Installation

1. Navigate to the desired folder and clone this repository:

    ```sh
    git clone https://github.com/StablePeru/AsRecorded.git
    cd AsRecordedAPP
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    ```

    2.1 On **Mac** and **Linux**:

    ```sh
    source venv/bin/activate
    ```

    2.2 On **Windows**:

    ```sh
env\Scripts ctivate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. If you have issues installing any dependency, make sure `pip` is updated:

    ```sh
    python -m pip install --upgrade pip
    ```

5. Run the application:

    ```sh
    python main.py
    ```

## Usage

1. Run the application:

    ```sh
    python main.py
    ```

2. Use the interface to load and edit Excel files, navigate between takes and characters, and mark interventions as complete.

## Contributing

If you wish to contribute to this project, follow these steps:

1. Fork the project.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## Resources
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or suggestions, please contact stableperu@gmail.com.
