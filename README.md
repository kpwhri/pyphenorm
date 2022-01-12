[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div>
  <p>
    <a href="https://github.com/kpwhri/pyphenorm">
      <img src="images/logo.png" alt="Logo">
    </a>
  </p>

<h3 align="center">pyphenorm</h3>

  <p>
    Python implementation of pyphenorm (forthcoming), and instructions for using AFEP. 
  </p>
</div>


<!-- TABLE OF CONTENTS -->

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## About the Project

Plan to eventually implement PheNORM algorithm.

Currently only supports running of AFEP from Metamaplite's json output. For original article,
see: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4986664/.

For help running Metamaplite, see: https://github.com/kpwhri/batch_metamaplite


<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.10+ (earlier might work)
* pyphenorm package: https://github.com/kpwhri/pyphenorm

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/kpwhri/pyphenorm.git
    ```
2. Install requirements (`pip install .[dev]` for test packages)
    ```sh
    pip install .
    ```
4. Run tests.
    ```sh
    set/export PYTHONPATH=src
    pytest tests
    ```

## Usage

Will eventually implement PheNORM algorithm. Currently only supports running of AFEP from Metamaplite's json output.

For help running Metamaplite, see: https://github.com/kpwhri/batch_metamaplite

### AFEP

1. Download text of relevant sites

## Versions

Uses [SEMVER](https://semver.org/).

See https://github.com/kpwhri/pyphenorm/releases.

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/kpwhri/pyphenorm/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License.

See `LICENSE` or https://kpwhri.mit-license.org for more information.


<!-- CONTACT -->

## Contact

Please use the [issue tracker](https://github.com/kpwhri/pyphenorm/issues).


<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

### Phenorm

* PheNorm implementation based on paper by Yu et al, J Am Med Inform Assoc. 2018 Jan; 25(1): 54–60.
    * Paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6251688/
    * Code: https://github.com/celehs/PheNorm

### SAFE

* SAFE implmentation based on paper by Yu et al, J Am Med Inform Assoc. 2015 Sep; 22(5): 993–1000.
    * Paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4986664/

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/kpwhri/pyphenorm.svg?style=flat-square

[contributors-url]: https://github.com/kpwhri/pyphenorm/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/kpwhri/pyphenorm.svg?style=flat-square

[forks-url]: https://github.com/kpwhri/pyphenorm/network/members

[stars-shield]: https://img.shields.io/github/stars/kpwhri/pyphenorm.svg?style=flat-square

[stars-url]: https://github.com/kpwhri/pyphenorm/stargazers

[issues-shield]: https://img.shields.io/github/issues/kpwhri/pyphenorm.svg?style=flat-square

[issues-url]: https://github.com/kpwhri/pyphenorm/issues

[license-shield]: https://img.shields.io/github/license/kpwhri/pyphenorm.svg?style=flat-square

[license-url]: https://kpwhri.mit-license.org/

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/company/kaiser-permanente-washington
<!-- [product-screenshot]: images/screenshot.png -->
