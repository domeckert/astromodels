__author__ = 'giacomov'

import collections
import numpy

from astromodels.sources.source import Source
from astromodels.sky_direction import SkyDirection
from astromodels.spectral_component import SpectralComponent
from astromodels.utils.pretty_list import dict_to_list
from astromodels.tree import Node

PARTICLE_SOURCE = 'particle source'


class ParticleSource(Source, Node):
    """
    A source of particles with a certain distribution. This source does not produce any electromagnetic signal,
    but it is useful if used in conjuction with spectral shapes which need a particle distribution as input, like
    for example a Synchrotron kernel.

    :param name: name for the source
    :param distribution_shape: a function describing the energy distribution of the particles
    :param components: a list of SpectralComponents instances
    :return:

    """

    def __init__(self, name, distribution_shape=None, components=None):

        Node.__init__(self, name)

        if components is None:

            assert distribution_shape is not None, "You have to either provied a list of components, or a " \
                                                   "distribution shape"

            components = [SpectralComponent("main", distribution_shape)]

        Source.__init__(self, components, PARTICLE_SOURCE)

        # Add a node called 'spectrum'

        spectrum_node = Node('spectrum')
        spectrum_node.add_children(self._components.values())

        self.add_child(spectrum_node)

        self.__call__ = self.get_flux

    def get_flux(self, energies):

        """Get the total flux of this particle source at the given energies (summed over the components)"""

        results = [component.shape(energies) for component in self.components.values()]

        return numpy.sum(results, 0)

    def _repr__base(self, rich_output=False):
        """
        Representation of the object

        :param rich_output: if True, generates HTML, otherwise text
        :return: the representation
        """

        # Make a dictionary which will then be transformed in a list

        repr_dict = collections.OrderedDict()

        key = '%s (particle source)' % self.name

        repr_dict[key] = collections.OrderedDict()
        repr_dict[key]['spectrum'] = collections.OrderedDict()

        for component_name, component in self.components.iteritems():

            repr_dict[key]['spectrum'][component_name] = component.to_dict(minimal=True)

        return dict_to_list(repr_dict, rich_output)