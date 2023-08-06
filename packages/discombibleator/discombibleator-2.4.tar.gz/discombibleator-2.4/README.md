# Discombibleator
## Creating a python program and dashboard to put ancient measurements in context

This tool will take in short strings of Ancient Hebrew and Caananite measurements and convert them to modern imperial or metric equivalents. Measures include time (hours and watches), length, weight, and volume (cubits, baths, etc.), and money (drachmae, etc).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This tool requires the following packages to be installed:
* Numpy
* Pandas
* NLTK
* Unittest (if running .test)

All are available in the standard Conda distributions. To make sure your distribution is up to date navigate to your terminal and type:

```
conda update conda
```

If you do not have Anaconda installed on your system, you can find it [here](https://anaconda.org).

### Installing

**Optional:**
Optionally, you may want to create a new Conda envionrment in which to run the program. If you choose to do this, you will need Anaconda in addition to the packaged outlined above. To launch an environment, type:

```
conda create -n discombibleator python =3.5 anaconda
```
And hit enter. After this, type this to activate your environment:

```
source activate discombibleator
```

**Not Optional:**
This program is available to pip install from Pypi. To install, simply navigate to your terminal and run the following (assuming your current environment has all the above packages available):

```
pip install discombibleator
```
That's it! The discombibleator is not available for you to start using in Jupyter Notebooks, text editors, or straight in Python on your terminal.

### Running Tests

Tests are available in the test file. To run them, simply change your directory to the package files and type:

```
python -m unittest
```

The tool's been tested before release, so these tests should all run without an error.

## Using the tool

To use the tool, run python in your terminal with the following command (unless you';re running this in a notebook or text editor):

```
python
```

Then, import the package's tools with the following command:

```
from discombibleator import *
```

Type the following with your passage or measurement inside the "Verse" class parentheses:

```
Discombibleator(Verse("my verse here")).run()
```

And the tool should return the verse with ancient measurements converted to modern units.

### Special Note for Metric System Users

To get units in metric rather than imperial units, simply put `, "metric"` after the passage or measurement as follows:

```
Discombibleator(Verse("my verse here", "metric")).run()
```

### Limitations of Tool

This tool takes in passages, not verse references. Therefore, something like *"2 homers of oil"* will execute correctly, whereas *"Genesis 1:1"* will not. Additionally:
* *Bath*,*reed*, and *finger* are ancient units of measurement. There's no way currently for this tool to distinguish between synonyms, so references to water baths, plant reeds, and hand fingers will currently change their names to gallons and inches respectively.
* This tool only recognizes numbers written in digits. For example, *"12 bekahs"* will convert correctly, but
*"twelve bekahs"* will not. Although the name *"bekah"* will change, the string *"twelve"* will not, rendering an incorrect output. In most cases, this will throw a helpful error, indicating the tool has not found a valid measurement in the input.
* **On the other hand, this tool does except "the", "an", and "a" in front of measure words.** This is meant to make the tool more robust if the user inputs something like *"A Sabbath day's journey"* or *"A talent of gold"*, but best practice is still to put in *"1 Sabbath day's journey"* or *"1 talent of gold"*.

## Author

Brian Friederich - *Data Scientist, Booz Allen Hamilton*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
