# dftparse ![Develop status](https://travis-ci.org/CitrineInformatics/dftparse.svg?branch=develop) ![Pypi stats](https://img.shields.io/pypi/v/dftparse.svg)

Local, unopinionated parsers for DFT codes.

`dftparse` simply extracts key-value pairs from the inputs and outputs of dft codes by reading one or a few consecutive lines and putting the results into a list of dicts.
Repeated keys are repeated, preserving context through ordering.
It does not change the names to make them consistent across dft codes, nor does it do processing to homogenize units or basis.
`dftparser` is intended to be a building block for building more expressive or useful dft tools, such as [pif-dft](https://github.com/CitrineInformatics/pif-dft)

## Currently supported codes
 - VASP
 - PWSCF (Quantum Espresso)
