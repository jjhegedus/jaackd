# jaackd-freecad is tooling for extending and improving the functionality of FreeCad and integrating it with other jaackd systems

# FreeCAD Integration for Jaackd

This directory contains scripts and tools for extending and improving the functionality of FreeCAD, and integrating it with other Jaackd systems.

## Directory Structure

- `developer-notebook.md`: Documentation for developers on how to integrate custom functionality with FreeCAD.
- `install.py`: Script to install the Jaackd FreeCAD module.
- `jaackd-freecad/`: Directory containing the main FreeCAD module.
  - `commands/`: Contains custom FreeCAD commands.
  - `resources/`: Contains resources such as icons and translations.
  - `testing/`: Contains tests for the FreeCAD module.
  - `document_object.py`: Script for handling FreeCAD document objects.
  - `jaackd_freecad.py`: Main script for initializing the Jaackd FreeCAD workbench.
- `run_freecad.bat`: Batch file to run FreeCAD with the Jaackd module.
- `sample_debug.py`: Sample script for debugging.
- `utils/`: Utility scripts and tools.

## Installation

To install the Jaackd FreeCAD module, run the `install.py` script:

```sh
python install.py
```

## Usage

To use the Jaackd FreeCAD module, start FreeCAD and activate the Jaackd workbench:

1. Open FreeCAD.
2. Activate the Jaackd workbench from the workbench selector.

## Development

For development and testing, refer to the `developer-notebook.md` for detailed instructions on integrating custom functionality with FreeCAD.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](../CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Contact

For questions or support, please contact Jeff Hegedus at jeff@22ndtech.com.