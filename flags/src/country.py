from src.json_data import (load_json,save_json)
import unicodedata

class Country:
    def __init__(self,json_path,images_path):
        self._json = json_path
        self._impath = images_path
        self._urls = load_json(json_path,images_path)
    
    def search_function(self,search):
        srch = self.remove_accents(search).lower()
        matched = set()
        for name in self._urls:
            contry = self.remove_accents(name).lower()
            if srch in contry:
                matched.add(name)
        return matched


    def remove_accents(self,input_str):
        output_str = input_str
        if not input_str.isascii():
            nfkd_form = unicodedata.normalize('NFKD',input_str)
            output_str = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return output_str


    def search_function_levenshetein(self,search):
        srch = self.remove_accents(search).lower()
        if srch == "":
            return set([name for name in self._urls])
        costs = {}
        ifstarts = set()
        for name in self._urls:
            contry = self.remove_accents(name).lower()
            if contry.startswith(srch):
                ifstarts.add(name)
                continue

            m = len(srch) + 1
            n = len(contry) + 1
            zero = [0 for _ in range(m)]
            matrix = [[j for j in range(m)] if i == 0 else zero.copy() for i in range(n)]
            for i in range(n):
                matrix[i][0] = i

            for i in range(1,n):
                for j in range(1,m):
                    cost = 0 if contry[i-1] == srch[j-1] else 1
                    matrix[i][j] = min(
                        matrix[i-1][j] + 1, #deletion
                        matrix[i][j-1] + 1, #Insertion
                        matrix[i-1][j-1] + cost #Substitution
                    )

                    if i > 1 and j > 1 and contry[i-1] == srch[j-1] and contry[i-2] == srch[j-2]: #Transpositions
                        matrix[i][j] = min(matrix[i][j], matrix[i-2][j-2] + cost)

            distance = matrix[n-1][m-1]

            if distance not in costs:
                costs[distance] = [name]
            else:
                costs[distance].append(name)

        minimum = min(list(costs.keys()))
        return set(costs[minimum]).union(ifstarts)
            


    def get_state(self,name):
        return self._urls[name]
    
    def get_images(self):
        return self._impath

    def delete_for_names(self,to_delete,aux):
        return [aux[name] for name in to_delete]
    
    def put_to_used(self,name):
        self._urls[name] = True
        save_json(self._json,self._urls)