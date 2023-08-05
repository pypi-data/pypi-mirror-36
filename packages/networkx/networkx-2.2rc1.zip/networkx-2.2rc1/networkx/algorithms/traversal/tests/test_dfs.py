#!/usr/bin/env python
from nose.tools import *
import networkx as nx


class TestDFS:

    def setUp(self):
        # simple graph
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)])
        self.G = G
        # simple graph, disconnected
        D = nx.Graph()
        D.add_edges_from([(0, 1), (2, 3)])
        self.D = D

    def test_preorder_nodes(self):
        assert_equal(list(nx.dfs_preorder_nodes(self.G, source=0)),
                     [0, 1, 2, 4, 3])
        assert_equal(list(nx.dfs_preorder_nodes(self.D)), [0, 1, 2, 3])

    def test_postorder_nodes(self):
        assert_equal(list(nx.dfs_postorder_nodes(self.G, source=0)),
                     [3, 4, 2, 1, 0])
        assert_equal(list(nx.dfs_postorder_nodes(self.D)), [1, 0, 3, 2])

    def test_successor(self):
        assert_equal(nx.dfs_successors(self.G, source=0),
                     {0: [1], 1: [2], 2: [4], 4: [3]})
        assert_equal(nx.dfs_successors(self.D), {0: [1], 2: [3]})

    def test_predecessor(self):
        assert_equal(nx.dfs_predecessors(self.G, source=0),
                     {1: 0, 2: 1, 3: 4, 4: 2})
        assert_equal(nx.dfs_predecessors(self.D), {1: 0, 3: 2})

    def test_dfs_tree(self):
        exp_nodes = sorted(self.G.nodes())
        exp_edges = [(0, 1), (1, 2), (2, 4), (4, 3)]
        # Search from first node
        T = nx.dfs_tree(self.G, source=0)
        assert_equal(sorted(T.nodes()), exp_nodes)
        assert_equal(sorted(T.edges()), exp_edges)
        # Check source=None
        T = nx.dfs_tree(self.G, source=None)
        assert_equal(sorted(T.nodes()), exp_nodes)
        assert_equal(sorted(T.edges()), exp_edges)
        # Check source=None is the default
        T = nx.dfs_tree(self.G)
        assert_equal(sorted(T.nodes()), exp_nodes)
        assert_equal(sorted(T.edges()), exp_edges)

    def test_dfs_edges(self):
        edges = nx.dfs_edges(self.G, source=0)
        assert_equal(list(edges), [(0, 1), (1, 2), (2, 4), (4, 3)])
        edges = nx.dfs_edges(self.D)
        assert_equal(list(edges), [(0, 1), (2, 3)])

    def test_dfs_labeled_edges(self):
        edges = list(nx.dfs_labeled_edges(self.G, source=0))
        forward = [(u, v) for (u, v, d) in edges if d == 'forward']
        assert_equal(forward, [(0, 0), (0, 1), (1, 2), (2, 4), (4, 3)])

    def test_dfs_labeled_disconnected_edges(self):
        edges = list(nx.dfs_labeled_edges(self.D))
        forward = [(u, v) for (u, v, d) in edges if d == 'forward']
        assert_equal(forward, [(0, 0), (0, 1), (2, 2), (2, 3)])

    def test_dfs_tree_isolates(self):
        G = nx.Graph()
        G.add_node(1)
        G.add_node(2)
        T = nx.dfs_tree(G, source=1)
        assert_equal(sorted(T.nodes()), [1])
        assert_equal(sorted(T.edges()), [])
        T = nx.dfs_tree(G, source=None)
        assert_equal(sorted(T.nodes()), [1, 2])
        assert_equal(sorted(T.edges()), [])


class TestDepthLimitedSearch:

    def setUp(self):
        # a tree
        G = nx.Graph()
        nx.add_path(G, [0, 1, 2, 3, 4, 5, 6])
        nx.add_path(G, [2, 7, 8, 9, 10])
        self.G = G
        # a disconnected graph
        D = nx.Graph()
        D.add_edges_from([(0, 1), (2, 3)])
        nx.add_path(D, [2, 7, 8, 9, 10])
        self.D = D

    def dls_test_preorder_nodes(self):
        assert_equal(list(nx.dfs_preorder_nodes(self.G, source=0,
                                                depth_limit=2)), [0, 1, 2])
        assert_equal(list(nx.dfs_preorder_nodes(self.D, source=1,
                                                depth_limit=2)), ([1, 0]))

    def dls_test_postorder_nodes(self):
        assert_equal(list(nx.dfs_postorder_nodes(self.G,
                                                 source=3, depth_limit=3)), [1, 7, 2, 5, 4, 3])
        assert_equal(list(nx.dfs_postorder_nodes(self.D,
                                                 source=2, depth_limit=2)), ([3, 7, 2]))

    def dls_test_successor(self):
        result = nx.dfs_successors(self.G, source=4, depth_limit=3)
        assert_equal({n: set(v) for n, v in result.items()},
                     {2: {1, 7}, 3: {2}, 4: {3, 5}, 5: {6}})
        result = nx.dfs_successors(self.D, source=7, depth_limit=2)
        assert_equal({n: set(v) for n, v in result.items()},
                     {8: {9}, 2: {3}, 7: {8, 2}})

    def dls_test_predecessor(self):
        assert_equal(nx.dfs_predecessors(self.G, source=0, depth_limit=3),
                     {1: 0, 2: 1, 3: 2, 7: 2})
        assert_equal(nx.dfs_predecessors(self.D, source=2, depth_limit=3),
                     {8: 7, 9: 8, 3: 2, 7: 2})

    def test_dls_tree(self):
        T = nx.dfs_tree(self.G, source=3, depth_limit=1)
        assert_equal(sorted(T.edges()), [(3, 2), (3, 4)])

    def test_dls_edges(self):
        edges = nx.dfs_edges(self.G, source=9, depth_limit=4)
        assert_equal(list(edges), [(9, 8), (8, 7),
                                   (7, 2), (2, 1), (2, 3), (9, 10)])

    def test_dls_labeled_edges(self):
        edges = list(nx.dfs_labeled_edges(self.G, source=5, depth_limit=1))
        forward = [(u, v) for (u, v, d) in edges if d == 'forward']
        assert_equal(forward, [(5, 5), (5, 4), (5, 6)])

    def test_dls_labeled_disconnected_edges(self):
        edges = list(nx.dfs_labeled_edges(self.G, source=6, depth_limit=2))
        forward = [(u, v) for (u, v, d) in edges if d == 'forward']
        assert_equal(forward, [(6, 6), (6, 5), (5, 4)])
