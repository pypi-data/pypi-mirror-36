"""
Description: Pretty print an item
"""


from pprint import pprint
from mdatapipe.core import PipelinePlugin


class Plugin(PipelinePlugin):

    def on_input(self, item):
        pprint(item)
