# NumeriCal :abacus:

NumeriCal is a mathematical equation optimization and root-finding program developed by Musa Sina ERTUGRUL and Ikram Celal KESKIN.

## About

NumeriCal started as a lecture project by [Asc. Prof. Dr. Bora Canbula](https://github.com/canbula). It is designed to find roots of mathematical functions using the Fixed-Point Iteration Method and provides a graphical user interface (GUI) for interactive use.

## Features

- **Fixed-Point Iteration Method:** NumeriCal uses the Fixed-Point Iteration Method to find roots of mathematical functions.
- **Extremum Points:** The program identifies extremum points of the function.
- **Limits:** NumeriCal calculates limits at specific points for a given function.
- **Function Direction:** Determines whether the function is increasing or decreasing at specific points.
- **Custom Exceptions:** Includes custom exception classes like `NoAssumption` and `ImeginaryNumber`.
- **Web API:** The program can be run as a web API, accepting JSON inputs and responding with JSON results.
- **Graphical User Interface (GUI):** Provides an independent GUI for interacting with the API.

## Usage

To use NumeriCal, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/NumeriCal.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask web application:

    ```bash
    python app.py
    ```

4. Open a web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to use the GUI.

## Requirements

- Python 3
- Flask
- Numba
- SymPy
- NumPy
- Chart.js

## Contributing

Contributions to NumeriCal are welcome! If you want to contribute, you can start by checking the existing issues. Feel free to open a pull request.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Contact

For any inquiries or issues, feel free to contact the developers:

- Musa Sina ERTUGRUL: [GitHub](https://github.com/musasinaertugrul)
- Ikram Celal KESKIN: [GitHub](https://github.com/ikramcelalkeskin)

Happy coding with NumeriCal! :rocket:
