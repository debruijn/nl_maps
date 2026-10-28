from importlib.resources import files

from PIL import Image
import pytest

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


@pytest.mark.parametrize(
    ("mode", "background"),
    [
        ("RGB", (40, 50, 60)),
        ("RGBA", (40, 50, 60, 0)),
    ],
)
def test_add_to_existing_preserves_rgb_and_rgba_input_modes(tmp_path, mode, background):
    source = tmp_path / f"source-{mode}.png"
    output = tmp_path / f"with-bes-{mode}.png"
    Image.new(mode, PROVINCE_MAP_SIZE, background).save(source)

    add_to_existing(
        source,
        {
            "bonaire": [255, 255, 0],
            "saba": [255, 0, 255, 255],
            "statia": [0, 255, 255],
        },
        save_to=output,
    )

    with Image.open(output) as image:
        assert image.mode == mode
        assert image.getpixel((0, 0)) == background
        output_colors = {
            color
            for _, color in image.convert("RGB").getcolors(maxcolors=65536)
        }
        assert {(255, 255, 0), (255, 0, 255), (0, 255, 255)} <= output_colors
