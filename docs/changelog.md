# Changelog

All notable changes to the Nunyakata project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive documentation with Read the Docs
- Integration tracking system with GitHub Issues
- Development tools and CI/CD improvements

## [0.1.1] - 2025-01-27

### Added

- Complete Nalo Solutions integration
- Payment processing (MTN, Vodafone, AirtelTigo)
- SMS messaging with bulk support
- Email services with HTML and template support
- USSD session management
- Comprehensive test suite (56 tests, 67% coverage)
- Environment variable configuration support
- PyPI package distribution

### Features

- **Payment Services**

  - Mobile money payments
  - Payment callback handling
  - Multiple wallet support (MTN, Vodafone, AirtelTigo)
  - Transaction status tracking

- **SMS Services**

  - Single and bulk SMS sending
  - Custom sender ID support
  - Unicode message support
  - Phone number validation and formatting

- **Email Services**

  - Plain text and HTML emails
  - Bulk email sending
  - Email templates
  - Attachment support

- **USSD Services**
  - Interactive USSD sessions
  - Menu creation and navigation
  - Session state management
  - Custom USSD flows

### Technical

- Clean API design with consistent response formats
- Comprehensive error handling
- Request/response logging
- Type hints throughout codebase
- Extensive test coverage

## [0.1.0] - 2025-01-20

### Added

- Initial project structure
- Basic Nalo Solutions client
- Core payment functionality
- SMS sending capabilities
- Project documentation setup

---

## Release Notes

### Version 0.1.1 Highlights

This release marks the first stable version of Nunyakata with complete Nalo Solutions integration. Key achievements:

- **🏆 Production Ready**: All core services fully implemented and tested
- **📦 PyPI Available**: Easy installation with `pip install nunyakata`
- **🧪 Well Tested**: 56 comprehensive tests covering all functionality
- **📚 Documented**: Complete API documentation and examples
- **🔧 Developer Friendly**: Easy configuration and error handling

### Supported Ghana Services

- ✅ **Nalo Solutions** - Complete integration (Payments, SMS, Email, USSD)
- 🚧 **Hubtel** - Planned for v0.2.0
- 🚧 **ExpressPay** - Planned for v0.2.0
- 🚧 **PaySwitch** - Planned for v0.2.0

### Contributing

We welcome contributions! See our [Contributing Guide](contributing/setup.md) for details on:

- Adding new service integrations
- Improving documentation
- Writing tests
- Reporting issues

---

_For detailed technical changes, see the [commit history](https://github.com/SeveighTech/nunyakata/commits/main)._
