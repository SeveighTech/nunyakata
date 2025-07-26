# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-07-26

### Added

- Initial release of Nunyakata package
- Complete Nalo Solutions API integration:
  - Payment API with mobile money support
  - SMS API with GET/POST methods and dual authentication
  - USSD API with session management and menu creation
  - Email API with JSON/form formats and bulk sending
- Comprehensive test suite with 63 tests (100% pass rate)
- Support for both sandbox and production environments
- Multiple authentication methods (username/password and auth_key)
- Input validation and error handling
- Network resilience (timeout, retry, error handling)
- Type hints and full documentation
- GitHub Actions CI/CD pipeline
- Code coverage reporting

### Features

- **Payment Processing**: Secure mobile money payments with hash verification
- **SMS Messaging**: Send single and bulk SMS with multiple authentication options
- **USSD Services**: Interactive USSD menus with session management
- **Email Services**: Send emails with templates, attachments, and custom headers
- **Validation**: Phone number, email, and amount validation for Ghana
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Testing**: Production-ready with extensive test coverage

### Technical

- Python 3.8+ support
- Type hints throughout
- Modern Python packaging with hatchling
- Automated testing with pytest
- Code coverage with pytest-cov
- HTTP mocking with requests-mock
- GitHub Actions for CI/CD
