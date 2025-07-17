from collections import deque

def union(list1, list2):
    return list(dict.fromkeys(list1 + list2))

class Vert:
    def __init__(self, id):
        self.id = id
        self.labels = []

    def add_labels(self, new_labels):
        self.labels = union(self.labels, new_labels)

class Kripke:
    def __init__(self, vertex_num):
        self.size = vertex_num
        self.vertex = [Vert(i) for i in range(0, vertex_num)]
        self.edges = []

    def add_edges(self, new_edges):
        self.edges = union(self.edges, new_edges)
    
    def get_next(self,source):
        return [dest for (src,dest) in self.edges if src==source]
    
    def get_labels(self,source):
        return self.vertex[source].labels
    
    def get_reachable_states(self, start):
        visited = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for next_vert in self.get_next(current):
                if next_vert not in visited:
                    queue.append(next_vert)
        return visited
    