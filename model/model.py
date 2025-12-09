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
        minori=0
        maggiori=0
        if self.G.number_of_edges()==0:
            return 0,0
        for u,v,data in self.G.edges(data=True):
            peso=data['peso']
            if peso<soglia:
                minori=minori+1
            if peso>soglia:
                maggiori=maggiori+1

        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo(self,soglia:float):
        #restituisce il cammino minimo composto solo da archi con peso>soglia
        #versione con metodi networkx
        H=nx.Graph()
        for u,v,data in self.G.edges(data=True):
            if data['peso']>soglia:
                H.add_edge(u,v,peso=data['peso'])
        if H.number_of_edges()==0:
            return []
        percorso_migliore=[]
        peso_m=float('inf')
        for nodo_iniziale in H.nodes():
            for nodo_finale in H.nodes():
                if nodo_iniziale==nodo_finale:
                    continue
                try:
                   weighted_path =nx.shortest_path(H,source=nodo_iniziale,target=nodo_finale, weight="peso")
                   if len(weighted_path)<3:
                       continue
                   peso_tot=nx.shortest_path_length(H,source=nodo_iniziale,target=nodo_finale, weight="peso")
                   #aggiorno in base al miglior cammino
                   if peso_tot<peso_m:
                       peso_m=peso_tot
                       percorso_migliore=weighted_path
                except nx.NetworkXNoPath:
                    pass
        return percorso_migliore
    def cammino_minimo_ric(self,soglia:float):
        H=nx.Graph()
        for u,v,data in self.G.edges(data=True):
            if data['peso']>soglia:
                H.add_edge(u,v,peso=data['peso'])
        if H.number_of_edges()==0:
            return []
        migliore_cammino=None
        migliore_peso=float('inf')
        for nodo_iniziale in H.nodes():
            cammino,peso=self.dfs_ricorsiva(nodo_iniziale,
                                            {nodo_iniziale},
                                            [nodo_iniziale],
                                            0,
                                            H)
            if cammino is not None and peso<migliore_peso:
                migliore_cammino=cammino
                migliore_peso=peso
        return migliore_cammino

    def dfs_ricorsiva(self,nodo,visited, cammino, peso, H):
        if len(cammino)>=3:
            miglior_cammino=cammino.copy()
            peso_m=peso
        else:
            miglior_cammino = None
            peso_m = float('inf')
        for vicino in H.neighbors(nodo):
            if vicino not in visited:
                peso_arco=H[nodo][vicino]['peso']
                visited.add(vicino)
                cammino.append(vicino)

                sub_cammino,sub_peso=self.dfs_ricorsiva(
                    vicino,
                    visited,
                    cammino,
                    peso+peso_arco,
                    H
                )
                if sub_cammino is not None and sub_peso<peso_m:
                    peso_m=sub_peso
                    miglior_cammino=sub_cammino
                cammino.pop()
                visited.remove(vicino)
        return miglior_cammino,peso_m




















