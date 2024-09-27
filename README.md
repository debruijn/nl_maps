# Full Netherlands maps - Work In Progress
Create maps of the Netherlands that include the BES islands:
- append the islands to an existing map
- generate a new map (based on provinces or municipalities) that can also include the BES islands.

Status: Work in Progress! This is not yet ready for production, but if you want to take it for a spin as is, feel free
to try. Suggestions and questions are welcome!

## How to install and use
To install, you can use pip:
`pip install nl_maps`

A basic example of how to use this to update an existing figure:
```python
import nl_maps
input_picture = 'input.png'
bes_colors = {'bonaire': [255, 255, 0],
              'saba':    [255, 255, 0],
              'statia':  [0, 255, 0]}
nl_maps.add_to_existing(input_picture, bes_colors, save_to='output.png')
```
A basic example of how to use this to generate a figure from scratch:
```python
import nl_maps
nl_data = nl_maps.NLData(kind='provinces')  # Initialize with all provinces and BES islands set to 'N/A' and gray color
nl_data.update({'bonaire': 'Lived there', 'zuid-holland': 'Lived there', 'utrecht': 'Semi-lived there'})  
nl_maps.generate_map(nl_data, save_to='output.png')
```

### Extra configuration


## Motivation
To write

### Frequently Asked Questions
To write

## Licensing and modifications
The MIT License as included in `LICENSE` applies to all files in this repository outside the `source/` folder. For the
PNG files in that folder, separate licenses apply, as explained in `source/MODIFICATIONS.md` together with the changes
that have been applied to the original files.
