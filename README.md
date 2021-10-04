PHI-Canto documentation
=======================

Source files for the help pages of the PHI-Canto curation application. All
pages are written in Markdown and converted to MHTML files ([Mason][] Perl
templates) by a Python script (`compile_docs.py`). PNG images are compressed by
the [Pillow][] Python package.

Requirements
------------

* Python 3.6+
* [Markdown][] 3.3.*
* [lxml][] 4.6.*
* [Pillow][] 8.3.*

Instructions
------------

To build the documentation yourself, follow these steps:

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Make any changes to the source files in the `docs/` directory
4. Run the build script: `python3 compile_docs.py`

The built documentation will be output to the `build/` directory. These files
must be checked in to the main Canto repository at [pombase/canto][canto] before
the changes can be shown in PHI-Canto.

[canto]: https://github.com/pombase/canto
[Markdown]: https://pypi.org/project/Markdown/
[Mason]: https://metacpan.org/pod/Mason
[lxml]: https://pypi.org/project/lxml/
[Pillow]: https://pypi.org/project/Pillow/
