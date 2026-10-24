from collections import defaultdict


DEFAULT_COLORS = [[255, 0, 0, 255],
                  [0, 255, 0, 255],
                  [0, 0, 255, 255],
                  [255, 255, 0, 255],
                  [255, 0, 255, 255],
                  [0, 255, 255, 255],
                  [127, 0, 0, 255],
                  [0, 127, 0, 255],
                  [0, 0, 127, 255],
                  [127, 127, 0, 255],
                  [127, 0, 127, 255],
                  [0, 127, 127, 255],
                  [127, 255, 255, 255],
                  [255, 127, 255, 255],
                  [255, 255, 127, 255],
                  [127, 127, 255, 255],
                  [127, 255, 127, 255],
                  [255, 127, 127, 255],
                  [127, 255, 0, 255],
                  [255, 127, 0, 255],
                  [255, 0, 127, 255],
                  [127, 0, 255, 255],
                  [0, 127, 255, 255],
                  [0, 255, 127, 255] ]

rename = {'bon': 'bonaire', 'bo': 'bonaire', 'sab': 'saba', 'sta': 'statia', 'stat': 'statia', 'eus': 'statia',
          'eustatius': 'statia', 'st eustatius': 'statia', 'sint eustatius': 'statia',
          'zh': 'zuid-holland', 'nh': 'noord-holland', 'ut': 'utrecht', 'fr': 'friesland', 'gr': 'groningen',
          'dr': 'drenthe', 'li': 'limburg', 'nb': 'noord-brabant', 'ov': 'overijssel', 'fl': 'flevoland',
          'ze': 'zeeland',
          'adam': 'amsterdam', 'rdam': 'rotterdam', 'sdam': 'schiedam', 'dh': 'den haag', 'haag': 'den haag',
          'other': 'other'}  # Other is a hack


class NLData:

    def __init__(self, kind='provinces', include_bes=True):
        if kind == 'municipalities':
            raise NotImplementedError("Municipality-level map generation is not implemented.")
        if kind not in ('provinces', 'none'):
            raise ValueError("kind must be 'provinces' or 'none'.")

        self.kind = kind
        self.include_bes = include_bes
        self.color_mapping = defaultdict(lambda: DEFAULT_COLORS[len(self.color_mapping)])
        self.color_mapping['N/A'] = [127, 127, 127, 255]
        self.mapping = {}
        if self.kind == 'provinces':
            self._init_provinces()
        if self.include_bes:
            self._init_bes()


    def _init_provinces(self):
        province_mapping = {k: 'N/A' for k in ['zuid-holland', 'noord-holland', 'utrecht', 'zeeland', 'noord-brabant',
                                               'limburg', 'gelderland', 'flevoland', 'overijssel', 'drenthe',
                                               'friesland', 'groningen']}
        self._auto_update_colors(province_mapping)
        return {}

    def _init_bes(self):
        bes_mapping = {k: 'N/A' for k in ['bonaire', 'saba', 'statia']}
        self._auto_update_colors(bes_mapping)

    def _auto_update_colors(self, apply_mapping=None):
        if apply_mapping:
            for k, v in apply_mapping.items():
                # self.mapping[k] = [v, self.color_mapping[v]]
                self.mapping[k] = v
        else:  # TODO: consider to remove below since it is now doing nothing and a remainder from an older setup
            for k, v in self.mapping.items():
                pass  # self.mapping[k] = [v, self.color_mapping[v]]


    def _get_full_mapping(self, mapping):
        mapping = dict(mapping)
        if 'bes' in mapping:
            mapping['bonaire'] = mapping['bes']
            mapping['saba'] = mapping['bes']
            mapping['statia'] = mapping['bes']
            del mapping['bes']
        normalized_mapping = {}
        for region, value in mapping.items():
            if not isinstance(region, str):
                raise ValueError(f"Region names must be strings, got {region!r}.")
            name = region.lower()
            normalized_name = name if name in self.mapping or name == 'other' else rename.get(name)
            if normalized_name not in self.mapping and normalized_name != 'other':
                supported_regions = ', '.join(sorted(self.mapping))
                raise ValueError(
                    f"Unknown or unsupported region {region!r}. "
                    f"Supported regions: {supported_regions}."
                )
            normalized_mapping[normalized_name] = value
        if 'other' not in normalized_mapping:
            return normalized_mapping
        return {region: normalized_mapping.get(region, normalized_mapping['other'])
                for region in self.mapping}

    def update(self, update_dict):
        update_dict = self._get_full_mapping(update_dict)
        self._auto_update_colors(update_dict)
        self.mapping.update(update_dict)

    def get_categories(self):
        categories = dict(self.color_mapping)
        for category in self.mapping.values():
            if category not in categories:
                categories[category] = self.color_mapping[category]
        return categories

    def set_colors(self, color_dict):
        self.color_mapping.update(color_dict)
        self._auto_update_colors()