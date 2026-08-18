from typing import Dict

class Graph:
    def __init__(self, numRules: int):
        self.adj = {}
        self.visited = {}
        self.postorder = []
        for i in range(numRules):
            self.adj[i] = set()
            self.visited[i] = False
    
    def add_edge(self, point_from: int, point_to: int):
        self.adj[point_from].add(point_to)
    
    def __str__(self):
        r_str = ""
        for i in range(len(self.adj)):
            temp_list = [str(num) for num in self.adj[i]]
            if not temp_list:
                r_str += f"R{i}:\n"
            else:
                r_str += f"R{i}:R{',R'.join(temp_list)}\n"
        return r_str

    def make_reverse(self) -> "Graph":
        new_graph = Graph(len(self.adj))
        for i in range(len(self.adj)):
            for num in self.adj[i]:
                new_graph.add_edge(num, i)
        return new_graph
    
    def dfs(self, start_point):
        # Run a search that ends completely when all available nodes are visited
        self.visited[start_point] = True
        for point in self.adj[start_point]:
            if not self.visited[point]:
                self.dfs(point)
        self.postorder.append(start_point)
        return
    
    def dfs_forest(self):
        # Run a search that continues in numerical order if a tree is completely visited
        for i in range(len(self.adj)):
            self.visited[i] = False
        self.postorder = []
        
        for i in range(len(self.adj)):
            if not self.visited[i]:
                self.dfs(i)
    
    def dfs_scc(self, start_point):
        dfs_set = set()
        self.visited[start_point] = True
        for point in self.adj[start_point]:
            if not self.visited[point]:
                dfs_set = dfs_set.union(self.dfs_scc(point))
        dfs_set.add(start_point)
        return dfs_set
    
    def dfs_forest_scc(self, postorder: list[int]) -> list[set]:
        for i in range(len(self.adj)):
            self.visited[i] = False
        
        scc_list = []
        for i in postorder:
            if not self.visited[i]:
                scc_list.append(self.dfs_scc(i))
        return scc_list