# Changelog

Notable changes to `nl_maps` are recorded here. The 0.1.0 and 0.2.0 entries are reconstructed from repository history:
the project metadata was first set to 0.1.0, then changed to 0.2.0 in a commit titled as a release. The repository has no
Git tags or other evidence confirming which versions were published, so these entries describe the code history and do
not prove distribution.

## [Unreleased]

### Added
- Automated tests for region data handling and both public map-generation workflows.
- GitHub Actions checks for supported Python/Pillow combinations, package builds, and inclusion of map assets and license notices.

### Changed
- `NLData.get_categories()` returns the documented category-to-color mapping.
- Pillow 12.1.0 or later is required; image pixel access uses the non-deprecated Pillow API.
- Documentation now identifies province-level generation and adding BES to existing images as supported workflows.

### Fixed
- Invalid or unsupported region names now raise a descriptive `ValueError`.
- Municipality-level generation now raises a clear `NotImplementedError` instead of leaving an empty region mapping.

### Removed
- Removed the obsolete root-level `main.py` and `config.yml` prototype.

## [0.2.0]

### Added
- Added `add_to_existing()` to append the BES islands to an existing image, with per-island colors and configurable placement.
- Included the map assets and their license/attribution notices in package distributions.
- Added README usage examples and expanded project documentation.

## [0.1.0] (version metadata introduced in repository history)

### Added
- Initial Python package for generating province-level maps with category-based colors and the BES islands.
- Added `NLData` for initializing province and BES region mappings, updating categories, and overriding category colors.
- Added configurable map, island crop/placement, background, and output settings.
