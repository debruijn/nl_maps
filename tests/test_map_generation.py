from importlib.resources import files

from PIL import Image

from nl_maps import NLData, add_to_existing, generate_map


PROVINCE_MAP_SIZE = (1727, 2048)


def test_bundled_map_assets_are_available():
    package_files = files("nl_maps").joinpath("source")

    assert package_files.joinpath("nl_provinces.png").is_file()
    assert package_files.joinpath("bes_islands.png").is_file()


def test_generate_map_writes_a_colored_province_map(tmp_path):
    data = NLData(kind="provinces")
    data.update({"FR": "holiday"})
    output = tmp_path / "provinces.png"

    generate_map(data, save_to=output)

    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == PROVINCE_MAP_SIZE
        assert image.getpixel((750, 240)) == tuple(data.color_mapping["holiday"])


def test_add_to_existing_writes_map_with_colored_bes_islands(tmp_path):
    source = files("nl_maps").joinpath("source", "nl_provinces.png")
    output = tmp_path / "with_bes.png"
    colors = {
        "bonaire": [255, 255, 0],
        "saba": [255, 0, 255],
        "statia": [0, 255, 255],
    }

    add_to_existing(str(source), colors, save_to=output)

    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == PROVINCE_MAP_SIZE
        output_colors = {
            color
            for _, color in image.convert("RGB").getcolors(
                maxcolors=image.width * image.height
            )
        }
        assert all(tuple(color) in output_colors for color in colors.values())
