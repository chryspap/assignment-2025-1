
import sys
#----------------------------------
# Step 1: Creating the Nodes for specific number of zeros and ones
#----------------------------------

#Put O and 1 in the right order using backtracking until no zeros or ones are left
def addBack (output_nodes, current, zeros, ones):
    if zeros==0 and ones==0:
        output_nodes.append(current)
        return
    
    if ones>0 :
        addBack(output_nodes, current + [1], zeros, ones-1)

    if zeros>0:
        addBack(output_nodes, current + [0], zeros-1, ones)
   
#Create nodes 
def createNodes(zero_count, one_count):
    nodes = []
    addBack(nodes, [], zero_count, one_count)
    return nodes

#----------------------------------
#Step 2: Create Edges: Two nodes are neighbours if they differ by exactly one single transposition
#----------------------------------

#Check if two nodes are neighbours
def checkDiff(nodeA, nodeB):
    diff=0
    for a, b in zip(nodeA, nodeB):
        if a!=b:
            diff=diff+1
    if diff==2:
        return True #Loop would stop when this is true, 2 different positions result in a single transposition
    else:
        return False
    
#Edges would be represented in the form of a graph
def createEdges(nodes):
    graph = []
    for i in range(len(nodes)):
        node = {
            'node': nodes[i],
            'position': indices_rep(nodes[i]),
            'neighbours': []
        }
        for j in range(len(nodes)):
            if i != j:
                if checkDiff(nodes[i], nodes[j]):
                    node['neighbours'].append(nodes[j])
        graph.append(node)
    return graph

#----------------------------------
#Step 3: Positions Representation
#----------------------------------

def indices_rep(nodes):
    position = []
    length = len(nodes)
    i=0
    while i < length: #We keep the position where we find "1"
        if nodes[i] == 1:
            position.append(length-i-1)
        i = i + 1
    return position

# ----------------------------
# Step 4: Homogeneous and Genlex
# ----------------------------

def homogeneous(new_node, path):
    if len(path) > 0:
        return checkDiff(new_node, path[-1]['node'])
    return True

def genlex(current_pos, next_pos):
    for i in range(min(len(current_pos), len(next_pos))):
        if next_pos[i] > current_pos[i]:
            return True
        if next_pos[i] < current_pos[i]:
            return False
    return len(next_pos) > len(current_pos)

#----------------------------------
#Step 5: DFS search
#----------------------------------

def get_best_candidates(current, graph):
    candidates = []
    for node in graph:
        commons = 0
        for i in range(min(len(current['position']), len(node['position']))):
            if current['position'][i] == node['position'][i]:
                commons += 1
            else:
                break
        candidates.append({"node": node, "commons": commons})
    candidates.sort(key=lambda k: k['commons'])
    return candidates

def dfs(graph, current_node, visited, path):
    current_index = None
    for i in range(len(graph)):
        if graph[i]['node'] == current_node['node']:
            current_index = i
            break
    if current_index is None:
        return

    visited[current_index] = True
    path.append(current_node)

    candidates = get_best_candidates(current_node, graph)

    for candidate_info in reversed(candidates):  # From best to worst
        candidate = candidate_info['node']
        candidate_index = None
        for j in range(len(graph)):
            if graph[j]['node'] == candidate['node']:
                candidate_index = j
                break
        if candidate_index is not None and not visited[candidate_index]:
            if homogeneous(candidate['node'], path):
                dfs(graph, candidate, visited, path)
                break

#----------------------------------
#Step 6: Call mode as neceaary from command line
#----------------------------------

def binary(node):
    return int(''.join(str(bit) for bit in node), 2)


def main():

    zeros = int(sys.argv[1])
    ones = int(sys.argv[2])
    mode = sys.argv[3]

    nodes = createNodes(zeros, ones)
    graph = createEdges(nodes)

    if mode == "graph":
        for node in graph:
            node_id = binary(node['node'])
            neighbour_ids = [binary(neigh) for neigh in node['neighbours']]
            neighbour_ids.sort()
            print(f"{node_id} -> {neighbour_ids}")

    elif mode == "dfs":
        visited = [False] * len(graph)
        path = []

        dfs(graph, graph[0], visited, path)

        print(', '.join(''.join(str(bit) for bit in node['node']) for node in path))
        print(', '.join(''.join(str(p) for p in node['position']) for node in path))
        print(', '.join(str(binary(node['node'])) for node in path))

    else:
        print(f"Sorry does not exist: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
