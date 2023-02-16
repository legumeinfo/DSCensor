"""Controls the creation of a directed graph using networkx for DSCensor in memory object."""

import glob
import json
import os

import networkx as nx


class DirectedGraphController:
    """Imported by application to build and query directed graph"""

    def __init__(self, logger, dscensor_nodes="./autocontent"):
        self.logger = logger
        self.all_objects = {}  # collection of all objects for lookup in edge building
        self.dscensor_nodes = os.path.abspath(
            dscensor_nodes
        )  # directory to load object.json files from lis-autocontent populate-dscensor
        self.digraph = nx.DiGraph()  # initialize digraph
        self.parse_dscensor_nodes()
        self.generate_digraph()

    def parse_dscensor_nodes(self):
        """Read all object.json files from self.dscensor_nodes directory"""
        logger = self.logger
        dscensor_nodes = self.dscensor_nodes
        logger.info(f"Parsing DSCensor Nodes from: {dscensor_nodes}...")
        for dsnode in glob.glob(
            f"{dscensor_nodes}/*.json"
        ):  # find all json objects in dscensor_nodes directory
            logger.debug(dsnode)
            dsjson = None
            with open(dsnode, encoding="UTF-8") as nopen:
                dsjson = json.loads(nopen.read())
            logger.debug(dsjson)
            name = dsjson["filename"]
            self.all_objects[
                name
            ] = dsjson  # add object to self.all_objects for edge lookup later
            logger.debug(self.all_objects[name])

    def generate_digraph(self):
        """Create directed graph for use in DSCensor in memory service"""
        logger = self.logger
        digraph = self.digraph
        logger.info("Generating directed graph...")
        for name in self.all_objects:
            node = self.all_objects[name]
            logger.debug(node)
            if name in digraph:  # already added node as parent
                continue
            digraph.add_node(name, **node)  # add node and **attrs
            parents = node["derived_from"]
            logger.debug(parents)
            for parent in parents:
                if not parent:
                    continue
                parent_node = self.all_objects[parent]
                logger.debug(parent_node)
                digraph.add_node(parent, **parent_node)  # add parent and **attrs
                digraph.add_edge(name, parent)  # add derived_from edge equivalent

    def dump_nodes(self):
        """Dump digraph nodes as a list of dictionaries"""
        logger = self.logger
        logger.info("Dumping Nodes...")
        my_nodes = {"nodes": list(self.digraph.nodes(data=True))}
        return json.dumps(my_nodes, indent=4)

    def dump_edges(self):
        """Dump digraph edges as a list"""
        logger = self.logger
        logger.info("Dumping Edges...")
        my_edges = {"edges": list(self.digraph.edges())}
        return json.dumps(my_edges, indent=4)
