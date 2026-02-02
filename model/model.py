import copy
import networkx as nx
from database.dao import DAO
from geopy import distance

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._nodes = None
        self._edges = None
        self._conteggi = {}

    @staticmethod
    def get_years():

        years = []
        for item in DAO.get_years():
            years.append(item['year'])

        return years

    @staticmethod
    def get_shapes(year):

        shapes = DAO.get_shape_specific_year(year)

        result = []
        for item in shapes:
            result.append(item['shape'])

        return result

    def build_graph(self, shape, year):

        self._nodes = DAO.get_all_states()
        self.G.add_nodes_from(self._nodes)

        stati = {}
        for s in self._nodes:
            conteggio = DAO.get_count_specific_state(year, shape, s.id)
            self._conteggi[s.id] = conteggio
            stati[s.id] = s

        neighbors = DAO.get_neighbors()

        for n in neighbors:
            state1 = stati[n[0]]
            state2 = stati[n[1]]
            peso = self._conteggi[n[0]] + self._conteggi[n[1]]
            self.G.add_edge(state1, state2, weight=peso)

    def get_num_nodes_num_edges(self):
        num_nodes = len(self._nodes)
        num_edges = len(self.G.edges())
        return num_nodes, num_edges


    def sum_weights_nodes(self):

        diz = {}
        for n in self._nodes:
            num = 0
            vicini = list(self.G.neighbors(n))
            for v in vicini:
                num += self._conteggi[v.id]

            num += len(vicini)*self._conteggi[n.id]
            diz[n] = num

        return diz

    def add_distance_grafo(self):

        for u, v in self.G.edges():
            dist = distance.geodesic((u.lat, u.lng), (v.lat, v.lng)).km

            self.G[u][v]['distance'] = dist

    def percorso(self, nodo_partenza):

        self._best_path = []
        self._best_dist_total = 0

        parziale = [nodo_partenza]

        self._ricorsione(nodo_partenza, parziale)

        return self._best_path, self._best_dist_total

    def _ricorsione(self, nodo_corrente, parziale):

        dist_accumulata = self.get_dist_accumulata(parziale)

        if dist_accumulata > self._best_dist_total:
            self._best_dist_total = dist_accumulata
            self._best_path = copy.deepcopy(parziale)

        last_node = parziale[-1]

        if len(parziale) == 1:
            peso_ultimo_arco = -1
        else:
            peso_ultimo_arco = self.G[parziale[-2]][last_node]['weight']

        ammissibili = []
        for vicino in self.G.neighbors(nodo_corrente):
            peso_corrente = self.G[vicino][nodo_corrente]['weight']
            if (peso_corrente > peso_ultimo_arco) and (vicino not in parziale):
                ammissibili.append(vicino)

        for vicino in ammissibili:
            parziale.append(vicino)
            self._ricorsione(vicino, parziale)
            parziale.pop()

    def get_dist_accumulata(self, parziale):

        score = 0
        for i in range(0, len(parziale)-1):
            u = parziale[i]
            v = parziale[i+1]
            dist = self.G[u][v]['distance']
            score += dist

        return score

    def definitivo(self, nodo_partenza):

        best_path, best_distanza = self.percorso(nodo_partenza)

        diz = {}
        for i in range(len(best_path)-1):
            u = best_path[i]
            v = best_path[i+1]
            peso = self.G[u][v]['weight']
            distanza = self.G[u][v]['distance']
            ready = [peso, distanza]
            diz[(u, v)] = ready

        return diz, best_distanza

    def get_nodes(self):
        return self._nodes

