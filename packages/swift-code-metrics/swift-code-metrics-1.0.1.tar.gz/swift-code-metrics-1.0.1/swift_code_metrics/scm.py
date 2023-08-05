#!/usr/bin/python

from argparse import ArgumentParser
from ._analyzer import Inspector
from ._presenter import GraphPresenter
from .version import VERSION
import sys


def main():

    CLI = ArgumentParser(description='Analyzes the code metrics of a Swift project.')
    CLI.add_argument(
        '--source',
        metavar='S',
        nargs='*',
        type=str,
        default='',
        required=True,
        help='The root path of the Swift project.'
    )
    CLI.add_argument(
        '--artifacts',
        nargs='*',
        type=str,
        default='',
        required=True,
        help='Path to save the artifacts generated'
    )
    CLI.add_argument(
        '--exclude',
        nargs='*',
        type=str,
        default=[],
        help='List of paths to exclude from analysis (e.g. submodules, pods, checkouts)'
    )
    CLI.add_argument(
        '--generate-graphs',
        nargs='?',
        type=bool,
        const=True,
        default=False,
        help='Generates the graphic reports and saves them in the artifacts path.'
    )
    CLI.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + VERSION
    )

    args = CLI.parse_args()
    directory = args.source[0]
    exclude = args.exclude
    artifacts = args.artifacts[0]
    should_generate_graphs = args.generate_graphs

    # Inspects the provided directory
    analyzer = Inspector(directory, artifacts, exclude)

    if not should_generate_graphs:
        sys.exit(0)

    # Creates graphs
    graph_presenter = GraphPresenter(artifacts)

    # Sorted data plots
    sorted_data = {
        'N. of classes and structs': lambda fr: fr.number_of_concrete_data_structures,
        'Lines Of Code - LOC': lambda fr: fr.loc,
        'Number Of Comments - NOC': lambda fr: fr.noc,
        'N. of methods - NBM': lambda fr: fr.number_of_methods,
        'Instability - I': lambda fr: analyzer.instability(fr),
        'Abstractness - A': lambda fr: analyzer.abstractness(fr),
    }

    for title, framework_function in sorted_data.items():
        graph_presenter.sorted_data_plot(title, analyzer.frameworks, framework_function)

    # Distance from the main sequence
    graph_presenter.distance_from_main_sequence_plot(analyzer.frameworks,
                                                     lambda fr: analyzer.instability(fr),
                                                     lambda fr: analyzer.abstractness(fr))
