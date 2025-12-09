import networkx as nx
from database.dao import DAO
class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G=nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        lst_rifugi = DAO.leggi_rifugio(year)
        lst_connessione= DAO.leggi_connessione(year)
        self.idMap={r.id: r for r in lst_rifugi}
        #prendo i nodi
        self.G.add_nodes_from(lst_rifugi)
        for c in lst_connessione:
            r1=self.idMap[c.id_rifugio1]
            r2=self.idMap[c.id_rifugio2]
            if c.difficolta=='facile':
                fattore=1
            elif c.difficolta=='media':
                fattore=1.5
            else:
                fattore=2
            peso=float(c.distanza)*fattore
            self.G.add_edge(r1,r2,peso=peso)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        #verifichiamo che il grafo abbia gli archi
        if self.G.number_of_edges()==0:
            return None #se non ci sono archi non si possono trovare il peso massimo e minimo
        pesi=[]
        #estraiamo tutti i pesi
        for u,v,data in self.G.edges(data=True):
            #u rappresenta il nodo 1 dell'arco, v rappresenta il nodo 2 dell'arco, e data è un dizionario che contiene tutti gli attributi dell'arco
            peso=data['peso']
            pesi.append(peso)
        min_peso=min(pesi)
        max_peso=max(pesi)

        return min_peso, max_peso




    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
