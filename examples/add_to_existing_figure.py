# This script shows an example of how to use nl_maps to add the BES islands to an existing map of the Netherlands

from importlib.resources import as_file, files

import nl_maps

bes_data = {'bonaire': [255, 255, 0],
            'saba': [ 255, 255, 0],
            'statia': [0, 255, 0]}

# Use the bundled province map as an example input. as_file also works if package resources are not regular files.
source_pic = files("nl_maps").joinpath("source", "nl_provinces.png")
with as_file(source_pic) as source_path:
    # By default, BES will be placed in the top-left using the default layout.
    nl_maps.add_to_existing(source_path, bes_data, save_to="out/not-tweaked.png")

    # A Config object can override settings such as the BES island positions.
    config = nl_maps.Config()
    config.out_config.bes_locs = {
        "bonaire": [100, 50],
        "saba": [120, 200],
        "statia": [220, 350],
    }
    nl_maps.add_to_existing(
        source_path,
        bes_data,
        config=config,
        save_to="out/custom-layout.png",
    )
