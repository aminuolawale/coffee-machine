import math


class SuggestionsMixin:
    def _parse(self, word):
        valid_commands = ["report", "reset", "off"] + self.offerings
        most_similar = None
        curr_dist = math.inf
        for c in valid_commands:
            doc_distance = self._doc_distance(c, word)
            if doc_distance < curr_dist:
                curr_dist = doc_distance
                most_similar = c
        return most_similar

    def _doc_distance(self, word1, word2):
        """ """
        map1 = {}
        map2 = {}
        for l in word1:
            if not l in map1:
                map1[l] = 0
            map1[l] += 1
        for l in word2:
            if not l in map2:
                map2[l] = 0
            map2[l] += 1
        dist = math.acos(
            self._dot_product(map1, map2)
            / math.sqrt(self._dot_product(map1, map1) * self._dot_product(map2, map2))
        )
        return dist

    def _dot_product(self, map1, map2):
        sum = 0
        for key in map1:
            if key in map2:
                sum += map1[key] * map2[key]
        return sum