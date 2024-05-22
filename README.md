# TaskBot

# TaskBot

TaskBot is a task automation tool built using Python and tkinter. It provides a graphical user interface (GUI) for scripting and executing automated actions such as mouse clicks, keystrokes, and more. The tool is available in two versions: Basic and Advanced, catering to different user needs and complexity levels.

## Features

**TaskBot_Basic**:
- Load and execute actions from a JSON file.
- Basic GUI for action management.
- Execute automated tasks like mouse clicks, keyboard actions, etc.

**TaskBot_Advanced**:
- All features of the Basic version.
- Ability to save and manage actions in a JSON file through the GUI.
- Enhanced error handling and validation of user inputs.

## Installation

**Prerequisites**:
- Python 3.x
- `pyautogui`, `tkinter`, `sv_ttk`

First, clone the repository to your local machine:

```bash
git clone https://github.com/Xza85hrf/TaskBot.git
cd TaskBot

```
Install the required dependencies:
```bash
pip install -r requirements.txt

```
Usage
Navigate to either the Basic or Advanced version directory and run the main script:

For TaskBot_Basic:
```bash
cd TaskBot_Basic
python TaskBot_Basic.py
```
For TaskBot_Advanced:
```bash
cd TaskBot_Advanced
python TaskBot_Advanced.py

```
Configuration
Actions are defined in a JSON file format. Here’s a sample configuration:
```json
[
  {
    "type": "click",
    "position": [100, 200],
    "description": "Click at position"
  },
  {
    "type": "type",
    "text": "Hello, world!",
    "description": "Type some text"
  }
]
```
Load this file through the GUI to execute the described actions.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Known Issues

- Limited error handling in file operations.
- UI responsiveness can lag with extensive action lists.

## Future Enhancements

- Multi-language support.
- Integration with additional automation libraries.
- Real-time action editing and preview.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
