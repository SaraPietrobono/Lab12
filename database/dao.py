from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def leggi_connessione(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.id, LEAST(c.id_rifugio1, id_rifugio2) as id_rifugio1, 
                        GREATEST(c.id_rifugio1, c.id_rifugio2) as id_rifugio2, c.distanza, c.difficolta, c.durata, c.anno
                        FROM connessione as c
                        WHERE c.anno<=%s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def leggi_rifugio(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                    FROM rifugio as r, connessione as c
                    WHERE (r.id=c.id_rifugio1 or r.id=c.id_rifugio2) and c.anno<=%s

    """
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Rifugio(**row))
        cursor.close()
        conn.close()
        return result


