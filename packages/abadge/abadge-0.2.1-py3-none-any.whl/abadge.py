"""
abadge - generate badges/shields with pure HTML/CSS.



"""

label_css = '''
    background: #444;
    border-radius: 4px 0px 0px 4px;
    color: white;
    font-family: DejaVu Sans,Verdana,sans;
    font-size: 80%;
    padding: 4px 8px 4px 8px;
    text-shadow: 1px 1px black
}'''

value_css = '''
.badge-value {
    background: #2b2;
    border-radius: 0px 4px 4px 0px;
    color: white;
    font-family: DejaVu Sans,Verdana,sans;
    font-size: 80%;
    padding: 4px 8px 4px 8px;
    text-shadow: 1px 1px black
}
'''


class Badge(object):
    """
    Class which represent status badges/shields.

    This class can be instantiated to generate many badges with the same
    format::

        passed_badge = Badge(value_text_color='#11a')
        print(success_badge.to_html('build', 'passed'))
        print(success_badge.to_html('tests', 'ok'))

    or for one-shot generation::

        print(Badge(label='tests', value='4/8').to_html())
        print(Badge().to_html(label='tests', value='4/8'))  # Same thing
        print(Badge.make_badge(tests, '4/8'))               # This too

    """
    config = {
        'border_radius': '4px',
        'label': '',
        'label_background': '#444',
        'label_text_color': 'white',
        'label_text_shadow': '1px 1px black',
        'font_family': 'DejaVu Sans, Verdana, sans',
        'font_size': '80%',
        'padding': '4px 8px 4px 8px',
        'thresholds': {},
        'url': '',
        'value': '',
        'value_background': '#444',
        'value_text_color': 'white',
        'value_text_shadow': '1px 1px black',
    }

    template = '<span style="' \
               'background:{label_background};' \
               'border-radius:{border_radius} 0px 0px {border_radius};' \
               'color:{label_text_color};' \
               'font-family:{font_family};' \
               'font-size:{font_size};' \
               'padding:{padding};' \
               'text-shadow:{label_text_shadow};' \
               '">{label}</span>' \
               '<span style="' \
               'background:{value_background};' \
               'border-radius:0px {border_radius} {border_radius} 0px;' \
               'color:{value_text_color};' \
               'font-family:{font_family};' \
               'font-size:{font_size};' \
               'padding:{padding};' \
               'text-shadow:{value_text_shadow};' \
               '">{value}</span>'

    href_template = '<a href="{url}">'

    def __init__(self, *args, **kwargs):
        """
        Create a badge object with the given configuration.

        Most configuration options are simply CSS settings. Please visit the
        w3c site for detailed information about the values.

        Optional arguments:
        label -- text for the label (left) part
        value -- text for the value (right) part

        Keyword arguments:
        border_radius -- how rounded the corners of the badge should be
                        (CSS "padding")
        label -- the text in label part of the badge
        label_background -- background color for the label (left) part
                        (CSS "background")
        label_text_color -- text color for the label (left) part
                        (CSS "text-color")
        font_family -- font to use in the badge (CSS "font-family")
        padding -- amount of space between the border and the badge
                   (CSS "padding")
        text_shadow -- configuration for the text shadow (CSS "text-shadow")
        value -- the value part of the badge
        """
        self.config.update(self._parse_args(args, kwargs))
        if len(args) > 0:
            self.config['label'] = args[0]
        if len(args) > 1:
            self.config['value'] = args[1]

    @classmethod
    def _parse_args(cls, args, kwargs):
        """
        Parse kwargs and return a dict.
        :param kwargs: dict to parse
        :return:
        """
        if len(args) > 2:
            raise ValueError('a maximum of 2 optional argument may be given'
                             ' ({} were given.)'.format(len(args)))
        for k in kwargs.keys():
            if k not in cls.config:
                raise TypeError('unknown option {}'.format(k))
        return kwargs

    @classmethod
    def _get_value_background(cls, config):
        """
        Return the calculated background color based on the "value" key.

        :param config: the config dict
        :return: color string
        """
        if 'thresholds' in config:
            return config['thresholds'].get(config['value'],
                                            config['value_background'])
        return config['value_background']

    def to_html(self, *args, **kwargs):
        """
        Render HTML for this badge
        :return: string with HTML
        """
        config = self.config.copy()
        config.update(self._parse_args(args, kwargs))
        if len(args) > 0:
            config['label'] = args[0]
        if len(args) > 1:
            config['value'] = args[1]
        config['value_background'] = self._get_value_background(config)
        if config['url']:
            return self.href_template.format(**config) \
                   + self.template.format(**config) + '</a>'
        return self.template.format(**config)

    @classmethod
    def make_badge(cls, *args, **kwargs):
        """
        Return the HTML for the given
        :param kwargs:
        :return:
        """
        return Badge().to_html(*args, **kwargs)
