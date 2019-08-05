import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from clear import clear
import sys


class GraphLib():
    def read_xml_file(self, fileName="mapGraph.xml"):
        graph_file = open(fileName)
        nodesTree = ET.parse(graph_file)

        self.myGraph = nx.DiGraph()
        self.myGraphPositions = {}
        root = nodesTree.getroot();
        for child in root:
            for grandson in child:
                if grandson.tag == "NODE":
                    name = grandson.find("NAME").text
                    posx = grandson.find("XPOS").text
                    posy = grandson.find("YPOS").text
                    index = grandson.find("INDEX").text
                    self.myGraph.add_node(
                        int(index), name=name, pos=(float(posx), - float(posy)))
                    self.myGraphPositions[
                        int(index)] = (float(posx), - float(posy))
                elif grandson.tag == "EDGE":
                    startIndex = grandson.find("STARTINDEX").text
                    endIndex = grandson.find("ENDINDEX").text
                    cost = grandson.find("COST").text
                    self.myGraph.add_weighted_edges_from(
                        [(int(startIndex), int(endIndex), float(cost))])

        self.return_to_menu()

    def draw_graph_with_positions(self):
        labels = nx.get_node_attributes(self.myGraph, 'name')
        nx.draw(
            self.myGraph,
            self.myGraphPositions,
            with_labels=True,
            labels=labels)
        labels = nx.get_edge_attributes(self.myGraph, 'weight')
        nx.draw_networkx_edge_labels(
            self.myGraph,
            self.myGraphPositions,
            edge_labels=labels)
        plt.show()
        self.return_to_menu()

    def find_path_astar(self):
        start, end = self.read_start_end()
        astarPath = nx.astar_path(
            self.myGraph, start, end, heuristic=self.dist)
        self.draw_path(astarPath)

    def find_path_dijkstra(self):
        start, end = self.read_start_end()
        dijkstraPath = nx.dijkstra_path(
            self.myGraph, start, end)
        self.draw_path(dijkstraPath)

    def find_path_dfs(self):
        start, end = self.read_start_end()
        paths = nx.all_simple_paths(self.myGraph, source=start, target=end)
        self.draw_path(list(paths)[0])

    def find_path_bellman(self):
        start, end = self.read_start_end()
        bfPath = nx.bellman_ford_path(
            self.myGraph, start, end)
        self.draw_path(bfPath)

    def draw_path(self, path):
        print(path)
        for i in path:
            print(self.myGraph.nodes[i]['name'])
        nx.draw_networkx_edges(
            self.myGraph,
            pos=self.myGraphPositions,
            edgelist=self.generate_path(path),
            edge_color='b',
            width=5)
        self.draw_graph_with_positions()

    def read_start_end(self):
        start = 0
        start = self.read_node("starting ")
        end = 0
        end = self.read_node("goal ")
        return start, end

    def read_node(self, whichNode=""):
        x = input(
            "Enter name or number of " +
            whichNode + "node(list to list all nodes): ")
        if x == 'list':
            for i in range(len(self.myGraph)):
                print(str(i) + '.' + self.myGraph.nodes[i]['name'])
            return (self.read_node(whichNode))
        elif self.representsInt(x) and int(x) >= 0 and int(x) < len(self.myGraph.nodes):
            return int(x)
        else:
            try:
                labels = nx.get_node_attributes(self.myGraph, 'name')
                for iter in range(len(labels)):
                    if labels[iter] == x:
                        return iter
                input("Wrong name, press any key to return to menu")
                self.menu()
            except Exception as e:
                input("Wrong name, press any key to return to menu")
                self.menu()

    def representsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def generate_path(self, path):
        routes = []
        for i in range(len(path) - 1):
            routes.append([path[i], path[i + 1]])
        return routes

    def menu(self):
        clear()
        print("####MENU####")
        self.menuOptions = []
        self.menuOptions.append(('read_xml_file', "Read graph from XML file"))
        self.menuOptions.append(('draw_graph_with_positions', "Draw graph"))
        self.menuOptions.append(('find_path_astar', "Find path using A*"))
        self.menuOptions.append(('find_path_dijkstra', "Find path using Dijkstra"))
        self.menuOptions.append(('find_path_dfs', "Find path using DFS"))
        self.menuOptions.append(('find_path_bellman', "Find path using Bellman Ford method"))
        self.menuOptions.append(('exit', "Exit"))
        for i, j in enumerate(self.menuOptions):
            print(i, ". ", j[1])
        x = input("Enter number: ")
        if int(x) == 0:
            x = input("Enter file name (default: mapGraph.xml): ")
            if x == '':
                getattr(self, self.menuOptions[0][0])()
            else:
                getattr(self, self.menuOptions[0][0])(x)
        else:
            getattr(self, self.menuOptions[int(x)][0])()
        # locals()[self.menuOptions[int(x)][0]]()

    def return_to_menu(self):
        x = input("Return to menu? (nY): ")
        if x == 'n':
            return
        else:
            return self.menu()

    def exit(self):
        sys.exit()

    def dist(self, a, b):
        (x1, y1) = self.myGraph.nodes[a]['pos']
        (x2, y2) = self.myGraph.nodes[b]['pos']
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


graphi = GraphLib()
graphi.menu()
