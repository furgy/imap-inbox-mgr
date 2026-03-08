# Versioning

## Version Format
Semantic versioning in format `X.Y.Z`:
- X: Major version (breaking changes)
- Y: Minor version (new features, backward compatible)
- Z: Patch version (bug fixes)

## Version Source
Version is stored in `VERSION` file (simple format: X.Y.Z)

## Version Bump Rules
- Every push to `main` branch must include a version bump in VERSION file
- Version must follow semver format
- CI will fail if VERSION file is not updated on push to main
