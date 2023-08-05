import numpy as np


class SumProduct():
    """ Sum-product distributive law """


    def __init__(self, einsum, *args, **kwargs):
        # Perhaps support for different frameworks (TensorFlow, Theano) could
        # be provided by giving the necessary functions.
        self.func = einsum
        self.args = args
        self.kwargs = kwargs
        return

    def einsum(self, *args, **kwargs):
        return self.func(*args, *self.args, **kwargs, **self.kwargs)


    def project(self, clique_pot, clique_keys, sep_keys):
        """
        Compute sepset potential by summing over keys
            in clique not shared by separator

        Input:
        ------

        Clique potential

        Clique keys

        Separator keys

        Output:
        -------

        Updated separator potential

        """

        # map keys to get around variable count limitation in einsum
        mapped_keys = []
        m_keys = {}
        for i,k in enumerate(clique_keys):
            m_keys[k] = i
            mapped_keys.append(i)

        return self.einsum(
            clique_pot,
            mapped_keys,
            [m_keys[k] for k in sep_keys]
        )

    def absorb(self, clique_pot, clique_keys, sep_pot, new_sep_pot, sep_keys):
        """
        Compute new clique potential as product of old clique potential
            and quotient of new separator potential and old separator
            potential

        Input:
        ------

        Clique potential to be updated

        Clique keys

        Old separator potential

        New separator potential

        Separator keys

        Output:
        -------

        Updated clique potential

        """
        if np.all(sep_pot) == 0:
            return np.zeros_like(clique_pot)

        # map keys to get around variable count limitation in einsum
        mapped_keys = []
        m_keys = {}
        for i,k in enumerate(clique_keys):
            m_keys[k] = i
            mapped_keys.append(i)

        return self.einsum(
            new_sep_pot / sep_pot, [m_keys[k] for k in sep_keys],
            clique_pot, mapped_keys,
            mapped_keys
        )

    def update(self, clique1_pot, clique1_keys, clique2_pot, clique2_keys, sep_pot, sep1_keys, sep2_keys):
        """
        A single update (message pass) from clique1 to clique2
            through separator

        Input:
        ------

        Clique1 potential

        Clique1 keys

        Clique2 potential

        Clique2 keys

        Separator potential

        Separator keys mapped to clique1 keys

        Separator keys mapped to clique2 keys

        Output:
        -------

        Updated clique2 potential and updated separator potential

        """
        # See page 2:
        # http://compbio.fmph.uniba.sk/vyuka/gm/old/2010-02/handouts/junction-tree.pdf

        # Sum keys in A that are not in B
        new_sep_pot = self.project(
                                clique1_pot,
                                clique1_keys,
                                sep1_keys
        )

        # Compensate the updated separator in the clique
        new_clique2_pot = self.absorb(
                                clique2_pot,
                                clique2_keys,
                                sep_pot,
                                new_sep_pot,
                                sep2_keys
        )

        return (new_clique2_pot, new_sep_pot) # may return unchanged clique_a
                                             # too if it helps elsewhere
