# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [Unreleased]

## [2022.3] - 2022-03-10
### Added
- SMTP configuration options to allow external server usage
- Support for SMTPS and SMTP authetication
- Systemd units examples
### Changed
- Code updated to Python 3.10
### Fixed
- Fixed selenium and workalendar deprecated code

## [2019.1] - 2019-05-15
### Added
- Use workalendar to avoid notifications on holidays
### Changed
- Better webdriver checking and error handling
### Fixed
- Fixed webdriver_path argument in README

## [2019.1b2] - 2019-01-15
### Fixed
- Update branch name for documentation links

## [2019.1b1] - 2019-01-15
### Changed
- Rewrite the project in Python 3
- Made as a Python package
- Docs using Sphinx
- Arguments can be provided on the command-line or via a configuration file
- Users can customize the screenshot size
- The script auto-detects if ChromeDriver's binary is present in PATH
