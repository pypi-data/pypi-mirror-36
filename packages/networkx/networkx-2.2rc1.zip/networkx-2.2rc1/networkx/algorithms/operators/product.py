#    Copyright (C) 2011 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Authors:
#     Aric Hagberg <hagberg@lanl.gov>
#     Pieter Swart <swart@lanl.gov>
#     Dan Schult <dschult@colgate.edu>
#     Ben Edwards <bedwards@cs.unm.edu>
"""
Graph products.
"""
from itertools import product

import networkx as nx
from networkx.utils import not_implemented_for

__all__ = ['tensor_product', 'cartesian_product',
           'lexicographic_product', 'strong_product', 'power',
           'rooted_product']


def _dict_product(d1, d2):
    return dict((k, (d1.get(k), d2.get(k))) for k in set(d1) | set(d2))


# Generators for producting graph products
def _node_product(G, H):
    for u, v in product(G, H):
        yield ((u, v), _dict_product(G.nodes[u], H.nodes[v]))


def _directed_edges_cross_edges(G, H):
    if not G.is_multigraph() and not H.is_multigraph():
        for u, v, c in G.edges(data=True):
            for x, y, d in H.edges(data=True):
                yield (u, x), (v, y), _dict_product(c, d)
    if not G.is_multigraph() and H.is_multigraph():
        for u, v, c in G.edges(data=True):
            for x, y, k, d in H.edges(data=True, keys=True):
                yield (u, x), (v, y), k, _dict_product(c, d)
    if G.is_multigraph() and not H.is_multigraph():
        for u, v, k, c in G.edges(data=True, keys=True):
            for x, y, d in H.edges(data=True):
                yield (u, x), (v, y), k, _dict_product(c, d)
    if G.is_multigraph() and H.is_multigraph():
        for u, v, j, c in G.edges(data=True, keys=True):
            for x, y, k, d in H.edges(data=True, keys=True):
                yield (u, x), (v, y), (j, k), _dict_product(c, d)


def _undirected_edges_cross_edges(G, H):
    if not G.is_multigraph() and not H.is_multigraph():
        for u, v, c in G.edges(data=True):
            for x, y, d in H.edges(data=True):
                yield (v, x), (u, y), _dict_product(c, d)
    if not G.is_multigraph() and H.is_multigraph():
        for u, v, c in G.edges(data=True):
            for x, y, k, d in H.edges(data=True, keys=True):
                yield (v, x), (u, y), k, _dict_product(c, d)
    if G.is_multigraph() and not H.is_multigraph():
        for u, v, k, c in G.edges(data=True, keys=True):
            for x, y, d in H.edges(data=True):
                yield (v, x), (u, y), k, _dict_product(c, d)
    if G.is_multigraph() and H.is_multigraph():
        for u, v, j, c in G.edges(data=True, keys=True):
            for x, y, k, d in H.edges(data=True, keys=True):
                yield (v, x), (u, y), (j, k), _dict_product(c, d)


def _edges_cross_nodes(G, H):
    if G.is_multigraph():
        for u, v, k, d in G.edges(data=True, keys=True):
            for x in H:
                yield (u, x), (v, x), k, d
    else:
        for u, v, d in G.edges(data=True):
            for x in H:
                if H.is_multigraph():
                    yield (u, x), (v, x), None, d
                else:
                    yield (u, x), (v, x), d


def _nodes_cross_edges(G, H):
    if H.is_multigraph():
        for x in G:
            for u, v, k, d in H.edges(data=True, keys=True):
                yield (x, u), (x, v), k, d
    else:
        for x in G:
            for u, v, d in H.edges(data=True):
                if G.is_multigraph():
                    yield (x, u), (x, v), None, d
                else:
                    yield (x, u), (x, v), d


def _edges_cross_nodes_and_nodes(G, H):
    if G.is_multigraph():
        for u, v, k, d in G.edges(data=True, keys=True):
            for x in H:
                for y in H:
                    yield (u, x), (v, y), k, d
    else:
        for u, v, d in G.edges(data=True):
            for x in H:
                for y in H:
                    if H.is_multigraph():
                        yield (u, x), (v, y), None, d
                    else:
                        yield (u, x), (v, y), d


def _init_product_graph(G, H):
    if not G.is_directed() == H.is_directed():
        msg = "G and H must be both directed or both undirected"
        raise nx.NetworkXError(msg)
    if G.is_multigraph() or H.is_multigraph():
        GH = nx.MultiGraph()
    else:
        GH = nx.Graph()
    if G.is_directed():
        GH = GH.to_directed()
    return GH


def tensor_product(G, H):
    r"""Return the tensor product of G and H.

    The tensor product $P$ of the graphs $G$ and $H$ has a node set that
    is the tensor product of the node sets, $V(P)=V(G) \times V(H)$.
    $P$ has an edge $((u,v), (x,y))$ if and only if $(u,x)$ is an edge in $G$
    and $(v,y)$ is an edge in $H$.

    Tensor product is sometimes also referred to as the categorical product,
    direct product, cardinal product or conjunction.


    Parameters
    ----------
    G, H: graphs
     Networkx graphs.

    Returns
    -------
    P: NetworkX graph
     The tensor product of G and H. P will be a multi-graph if either G
     or H is a multi-graph, will be a directed if G and H are directed,
     and undirected if G and H are undirected.

    Raises
    ------
    NetworkXError
     If G and H are not both directed or both undirected.

    Notes
    -----
    Node attributes in P are two-tuple of the G and H node attributes.
    Missing attributes are assigned None.

    Examples
    --------
    >>> G = nx.Graph()
    >>> H = nx.Graph()
    >>> G.add_node(0, a1=True)
    >>> H.add_node('a', a2='Spam')
    >>> P = nx.tensor_product(G, H)
    >>> list(P)
    [(0, 'a')]

    Edge attributes and edge keys (for multigraphs) are also copied to the
    new product graph
    """
    GH = _init_product_graph(G, H)
    GH.add_nodes_from(_node_product(G, H))
    GH.add_edges_from(_directed_edges_cross_edges(G, H))
    if not GH.is_directed():
        GH.add_edges_from(_undirected_edges_cross_edges(G, H))
    return GH


def cartesian_product(G, H):
    r"""Return the Cartesian product of G and H.

    The Cartesian product $P$ of the graphs $G$ and $H$ has a node set that
    is the Cartesian product of the node sets, $V(P)=V(G) \times V(H)$.
    $P$ has an edge $((u,v),(x,y))$ if and only if either $u$ is equal to $x$
    and both $v$ and $y$ are adjacent in $H$ or if $v$ is equal to $y$ and
    both $u$ and $x$ are adjacent in $G$.

    Parameters
    ----------
    G, H: graphs
     Networkx graphs.

    Returns
    -------
    P: NetworkX graph
     The Cartesian product of G and H. P will be a multi-graph if either G
     or H is a multi-graph. Will be a directed if G and H are directed,
     and undirected if G and H are undirected.

    Raises
    ------
    NetworkXError
     If G and H are not both directed or both undirected.

    Notes
    -----
    Node attributes in P are two-tuple of the G and H node attributes.
    Missing attributes are assigned None.

    Examples
    --------
    >>> G = nx.Graph()
    >>> H = nx.Graph()
    >>> G.add_node(0, a1=True)
    >>> H.add_node('a', a2='Spam')
    >>> P = nx.cartesian_product(G, H)
    >>> list(P)
    [(0, 'a')]

    Edge attributes and edge keys (for multigraphs) are also copied to the
    new product graph
    """
    GH = _init_product_graph(G, H)
    GH.add_nodes_from(_node_product(G, H))
    GH.add_edges_from(_edges_cross_nodes(G, H))
    GH.add_edges_from(_nodes_cross_edges(G, H))
    return GH


def lexicographic_product(G, H):
    r"""Return the lexicographic product of G and H.

    The lexicographical product $P$ of the graphs $G$ and $H$ has a node set
    that is the Cartesian product of the node sets, $V(P)=V(G) \times V(H)$.
    $P$ has an edge $((u,v), (x,y))$ if and only if $(u,v)$ is an edge in $G$
    or $u==v$ and $(x,y)$ is an edge in $H$.

    Parameters
    ----------
    G, H: graphs
     Networkx graphs.

    Returns
    -------
    P: NetworkX graph
     The Cartesian product of G and H. P will be a multi-graph if either G
     or H is a multi-graph. Will be a directed if G and H are directed,
     and undirected if G and H are undirected.

    Raises
    ------
    NetworkXError
     If G and H are not both directed or both undirected.

    Notes
    -----
    Node attributes in P are two-tuple of the G and H node attributes.
    Missing attributes are assigned None.

    Examples
    --------
    >>> G = nx.Graph()
    >>> H = nx.Graph()
    >>> G.add_node(0, a1=True)
    >>> H.add_node('a', a2='Spam')
    >>> P = nx.lexicographic_product(G, H)
    >>> list(P)
    [(0, 'a')]

    Edge attributes and edge keys (for multigraphs) are also copied to the
    new product graph
    """
    GH = _init_product_graph(G, H)
    GH.add_nodes_from(_node_product(G, H))
    # Edges in G regardless of H designation
    GH.add_edges_from(_edges_cross_nodes_and_nodes(G, H))
    # For each x in G, only if there is an edge in H
    GH.add_edges_from(_nodes_cross_edges(G, H))
    return GH


def strong_product(G, H):
    r"""Return the strong product of G and H.

    The strong product $P$ of the graphs $G$ and $H$ has a node set that
    is the Cartesian product of the node sets, $V(P)=V(G) \times V(H)$.
    $P$ has an edge $((u,v), (x,y))$ if and only if
    $u==v$ and $(x,y)$ is an edge in $H$, or
    $x==y$ and $(u,v)$ is an edge in $G$, or
    $(u,v)$ is an edge in $G$ and $(x,y)$ is an edge in $H$.

    Parameters
    ----------
    G, H: graphs
     Networkx graphs.

    Returns
    -------
    P: NetworkX graph
     The Cartesian product of G and H. P will be a multi-graph if either G
     or H is a multi-graph. Will be a directed if G and H are directed,
     and undirected if G and H are undirected.

    Raises
    ------
    NetworkXError
     If G and H are not both directed or both undirected.

    Notes
    -----
    Node attributes in P are two-tuple of the G and H node attributes.
    Missing attributes are assigned None.

    Examples
    --------
    >>> G = nx.Graph()
    >>> H = nx.Graph()
    >>> G.add_node(0, a1=True)
    >>> H.add_node('a', a2='Spam')
    >>> P = nx.strong_product(G, H)
    >>> list(P)
    [(0, 'a')]

    Edge attributes and edge keys (for multigraphs) are also copied to the
    new product graph
    """
    GH = _init_product_graph(G, H)
    GH.add_nodes_from(_node_product(G, H))
    GH.add_edges_from(_nodes_cross_edges(G, H))
    GH.add_edges_from(_edges_cross_nodes(G, H))
    GH.add_edges_from(_directed_edges_cross_edges(G, H))
    if not GH.is_directed():
        GH.add_edges_from(_undirected_edges_cross_edges(G, H))
    return GH


@not_implemented_for('directed')
@not_implemented_for('multigraph')
def power(G, k):
    """Returns the specified power of a graph.

    The $k$th power of a simple graph $G$, denoted $G^k$, is a
    graph on the same set of nodes in which two distinct nodes $u$ and
    $v$ are adjacent in $G^k$ if and only if the shortest path
    distance between $u$ and $v$ in $G$ is at most $k$.

    Parameters
    ----------
    G : graph
        A NetworkX simple graph object.

    k : positive integer
        The power to which to raise the graph `G`.

    Returns
    -------
    NetworkX simple graph
        `G` to the power `k`.

    Raises
    ------
    ValueError
        If the exponent `k` is not positive.

    NetworkXNotImplemented
        If `G` is not a simple graph.

    Examples
    --------
    The number of edges will never decrease when taking successive
    powers:

    >>> G = nx.path_graph(4)
    >>> list(nx.power(G, 2).edges)
    [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
    >>> list(nx.power(G, 3).edges)
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    The `k`th power of a cycle graph on *n* nodes is the complete graph
    on *n* nodes, if `k` is at least ``n // 2``:

    >>> G = nx.cycle_graph(5)
    >>> H = nx.complete_graph(5)
    >>> nx.is_isomorphic(nx.power(G, 2), H)
    True
    >>> G = nx.cycle_graph(8)
    >>> H = nx.complete_graph(8)
    >>> nx.is_isomorphic(nx.power(G, 4), H)
    True

    References
    ----------
    .. [1] J. A. Bondy, U. S. R. Murty, *Graph Theory*. Springer, 2008.

    Notes
    -----
    This definition of "power graph" comes from Exercise 3.1.6 of
    *Graph Theory* by Bondy and Murty [1]_.

    """
    if k <= 0:
        raise ValueError('k must be a positive integer')
    H = nx.Graph()
    H.add_nodes_from(G)
    # update BFS code to ignore self loops.
    for n in G:
        seen = {}                  # level (number of hops) when seen in BFS
        level = 1                  # the current level
        nextlevel = G[n]
        while nextlevel:
            thislevel = nextlevel  # advance to next level
            nextlevel = {}         # and start a new list (fringe)
            for v in thislevel:
                if v == n:         # avoid self loop
                    continue
                if v not in seen:
                    seen[v] = level         # set the level of vertex v
                    nextlevel.update(G[v])  # add neighbors of v
            if k <= level:
                break
            level += 1
        H.add_edges_from((n, nbr) for nbr in seen)
    return H


@not_implemented_for('multigraph')
def rooted_product(G, H, root):
    """ Return the rooted product of graphs G and H rooted at root in H.

    A new graph is constructed representing the rooted product of
    the inputted graphs, G and H, with a root in H.
    A rooted product duplicates H for each nodes in G with the root
    of H corresponding to the node in G. Nodes are renamed as the direct
    product of G and H. The result is a subgraph of the cartesian product.

    Parameters
    ----------
    G,H : graph
       A NetworkX graph
    root : node
       A node in H

    Returns
    -------
    R : The rooted product of G and H with a specified root in H

    Notes
    -----
    The nodes of R are the Cartesian Product of the nodes of G and H.
    The nodes of G and H are not relabeled.
    """
    if root not in H:
        raise nx.NetworkXError('root must be a vertex in H')

    R = nx.Graph()
    R.add_nodes_from(product(G, H))

    R.add_edges_from(((e[0], root), (e[1], root)) for e in G.edges())
    R.add_edges_from(((g, e[0]), (g, e[1])) for g in G for e in H.edges())

    return R
